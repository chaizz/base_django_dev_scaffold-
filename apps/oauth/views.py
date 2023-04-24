from abc import ABCMeta, abstractmethod

import requests
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.oauth.models import SocialAccount
from apps.system.models import Users
from utils.c_restframework.c_response import JsonResponse, ErrorResponse
from utils.common.exception import OAuthException


class OAuthView(APIView, metaclass=ABCMeta):
    """
    第三方账号认证视图，该视图负责处理回调请求，获取用户信息。
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def get(self, request, *args, **kwargs):
        access_token = self.get_access_token(request)
        user_info = self.get_user_info(access_token)
        return self.authenticate(user_info)

    def get_access_token(self, request) -> dict:
        """
        从github返回的连接中获取 code。
        再根据code获取 access_token。
        :param request:
        :return:
            {
                'access_token': 'xxxxxxxxx',
                'token_type': 'bearer',
                'scope': ''
            }
        """
        code = request.query_params.get("code")
        if not code:
            raise OAuthException("无法获取供应商信息：code！")

        url = self.access_token_url
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        resp = requests.post(url, data, headers=headers, timeout=2)
        # 解析返回的json文本
        result = resp.json()
        if 'access_token' in result:
            return result
        else:
            raise OAuthException("认证失败！")

    def get_user_info(self, access_token_dict: dict) -> dict:
        """
        根据 获取用户信息
        :param access_token_dict:
            {
                'access_token': 'xxxxxxxxx',
                'token_type': 'bearer',
                'scope': ''
            }
        :return:
            {
                'login': 'xxxxx',
                'id': xxxxxxxx,
                'node_id': 'xxxxxx',
                'avatar_url': 'https://avatars.githubusercontent.com/u/xxxxxx?v=4',
                'gravatar_id': '',
                'url': 'https://api.github.com/users/xxx',
                'html_url': 'https://github.com/xxx',
                'followers_url': 'https://api.github.com/users/xxx/followers',
                'following_url': 'https://api.github.com/users/xxx/following{/other_user}',
                'gists_url': 'https://api.github.com/users/xxx/gists{/gist_id}',
                'starred_url': 'https://api.github.com/users/xxxxx/starred{/owner}{/repo}',
                'subscriptions_url': 'https://api.github.com/users/xxxxx/subscriptions',
                'organizations_url': 'https://api.github.com/users/xxxxx/orgs',
                'repos_url': 'https://api.github.com/users/xxxxx/repos',
                'events_url': 'https://api.github.com/users/xxxxx/events{/privacy}',
                'received_events_url': 'https://api.github.com/users/xxxxx/received_events',
                'type': 'User',
                'site_admin': False,
                'name': 'xxxxx',
                'company': None,
                'blog': 'www.xxxxx.com',
                'location': 'Hangzhou',
                'email': None,
                'hireable': None,
                'bio': 'Python/JavaScript\r\n',
                'twitter_username': None,
                'public_repos': 304,
                'public_gists': 111,
                'followers': 14,
                'following': 41,
                'created_at': '2017-11-28T05:00:49Z',
                'updated_at': '2023-04-21T06:00:07Z'
                                      }
        """

        access_token = access_token_dict["access_token"]
        token_type = access_token_dict["token_type"]
        # 根据Github的API规则， 获取用户信息，必须在请求头上携带Authorization: token/Bearer xxxxxxxxxx。
        headers = {
            "Authorization": f"{token_type} {access_token}"
        }
        resp = requests.get(self.user_api, headers=headers, timeout=2)
        return resp.json()

    def get_success_url(self):
        '获取登录成功后返回的网页'
        if 'next' in self.request.session:
            # 还记得在OAuthLoginView中保存到session里的next吗
            # next保存了用户登录前正在浏览的网站
            # 比如当用户想要评论某篇文章时需要登录
            # 这时next就应保存那篇文章的url
            # 等用户完成登录操作后，依然可以继续他的评论，而不是跳到其他网页去了
            return self.request.session.pop('next')
        else:
            # 没有next就只能返回主页
            return '/'

    def update_social(self, user: object, uid: str, social_info: dict) -> None:
        try:
            social_account = SocialAccount.objects.get(uid=uid)
        except SocialAccount.DoesNotExist:
            social_account = SocialAccount(
                user=user,
                uid=uid,
                open_id=social_info["open_id"],
                nickname=social_info["nickname"],
                account_type=social_info["account_type"],
                phone_number=social_info["phone_number"],
                avatar_url=social_info["avatar_url"],
                email=social_info["email"]
            )
        social_account.save()

    @abstractmethod
    def authenticate(self, user_info):
        """
        业务逻辑~
        :param user_info:
        :return:
        """
        return JsonResponse(msg="success!", data="")


class GitHubOAuthView(OAuthView):
    """
        github账号认证视图
    """
    access_token_url = 'https://github.com/login/oauth/access_token'
    user_api = 'https://api.github.com/user?access_token='
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_SECRET

    def authenticate(self, user_info):
        """
        业务逻辑~
        :param user_info:
        :return:
        """

        uid = user_info["id"]
        username = user_info["login"]
        avatar_url = user_info["avatar_url"]
        email = user_info["email"]

        if email:
            return ErrorResponse(msg="此Github帐户没有与之关联的电子邮件地址！")

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            user = Users.objects.create_user(username=username, email=email)

        refresh = RefreshToken.for_user(user)

        self.update_social(user, uid, {
            "open_id": user_info["node_id"],
            "nickname": user_info["login"],
            "account_type": "github",
            "phone_number": "",
            "avatar_url": user_info["avatar_url"]
        })

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "expire": refresh.access_token.payload['exp'],  # 有效期,
            "username": username,
            "email": email
        }
        return JsonResponse(msg="success!", data=data)


class DingTalkOAuthView(OAuthView):
    """
        钉钉账号认证视图
    """
    code_url = "https://login.dingtalk.com/oauth2/auth?redirect_uri=http%3A%2F%2F127.0.0.1%3A9000%2Fapi%2Fv1%2Fdingtalk&response_type=code&client_id=ding9xmy2navxhxxgsyl&scope=openid&state=1111&prompt=consent"
    access_token_url = 'https://api.dingtalk.com/v1.0/oauth2/userAccessToken'
    user_api = 'https://api.dingtalk.com/v1.0/contact/users/me'
    client_id = settings.DINGTALK_KEY
    client_secret = settings.DINGTALK_SECRET

    def get_access_token(self, request) -> dict:
        """
        从github返回的连接中获取 code。
        再根据code获取 access_token。
        :param request:
        :return:
            {
                'access_token': 'xxxxxxxxx',
                'token_type': 'bearer',
                'scope': ''
            }
        """
        code = request.query_params.get("authCode")
        state = request.query_params.get("state")
        if not code:
            raise OAuthException("无法获取供应商信息：code！")

        url = self.access_token_url
        headers = {'Content-Type': 'application/json'}
        data = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
            'code': code,
            "grantType": "authorization_code"
        }
        resp = requests.post(url, json=data, headers=headers, timeout=2)
        # 解析返回的json文本
        result = resp.json()
        if 'accessToken' in result:
            return result
        else:
            raise OAuthException("认证失败！")

    def get_user_info(self, access_token_dict: dict) -> dict:
        """
        根据 获取用户信息
        :param access_token_dict:
            {
                'access_token': 'xxxxxxxxx',
                'token_type': 'bearer',
                'scope': ''
            }
        :return:
            {

                "nick" : "zhangsan",
                "avatarUrl" : "https://xxx",
                "mobile" : "150xxxx9144",
                "openId" : "123",
                "unionId" : "z21xxxzpw0Yxxxx",
                "email" : "zhangsan@alixbaba-inc.com",
                "stateCode" : "86"
            }

        """

        access_token = access_token_dict["accessToken"]
        headers = {
            "x-acs-dingtalk-access-token": access_token
        }
        resp = requests.get(self.user_api, headers=headers, timeout=2)
        return resp.json()

    def authenticate(self, user_info):
        """
        业务逻辑~
        :param user_info:
         {
            'nick': '张三',
            'unionId': 'xxxx',
            'avatarUrl': '',
            'openId': 'xxxx',
            'mobile': '180xxxxxxxxxxx',
            'stateCode': '86',
            'email': 'zhangsna@163.com'
        }

        :return:
        """

        uid = user_info["unionId"]
        username = user_info["mobile"]
        nick = user_info["nick"]
        avatar_url = user_info["avatarUrl"]
        email = user_info.get('email')

        if not email:
            return ErrorResponse(msg="此钉钉帐户没有与之关联的电子邮件地址！")

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            user = Users.objects.create_user(username=username, email=email)

        refresh = RefreshToken.for_user(user)


        self.update_social(user, uid, {
            "open_id": user_info["openId"],
            "nickname": nick,
            "account_type": "dingtalk",
            "phone_number": user_info["mobile"],
            "avatar_url": user_info["avatarUrl"],
            "email": user_info["email"],
        })


        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "expire": refresh.access_token.payload['exp'],  # 有效期,
            "username": username,
            "email": email
        }
        return JsonResponse(msg="success!", data=data)
