import requests
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from utils.c_restframework.c_response import JsonResponse
from utils.common.exception import OAuthException


class OAuthView(APIView):
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
                'login': 'chaizz',
                'id': 34051653,
                'node_id': 'MDQ6VXNlcjM0MDUxNjUz',
                'avatar_url': 'https://avatars.githubusercontent.com/u/34051653?v=4',
                'gravatar_id': '',
                'url': 'https://api.github.com/users/chaizz',
                'html_url': 'https://github.com/chaizz',
                'followers_url': 'https://api.github.com/users/chaizz/followers',
                'following_url': 'https://api.github.com/users/chaizz/following{/other_user}',
                'gists_url': 'https://api.github.com/users/chaizz/gists{/gist_id}',
                'starred_url': 'https://api.github.com/users/chaizz/starred{/owner}{/repo}',
                'subscriptions_url': 'https://api.github.com/users/chaizz/subscriptions',
                'organizations_url': 'https://api.github.com/users/chaizz/orgs',
                'repos_url': 'https://api.github.com/users/chaizz/repos',
                'events_url': 'https://api.github.com/users/chaizz/events{/privacy}',
                'received_events_url': 'https://api.github.com/users/chaizz/received_events',
                'type': 'User',
                'site_admin': False,
                'name': 'chaizz',
                'company': None,
                'blog': 'www.chaizz.com',
                'location': 'Hangzhou',
                'email': None,
                'hireable': None,
                'bio': 'Python/JavaScript\r\n',
                'twitter_username': None,
                'public_repos': 34,
                'public_gists': 1,
                'followers': 1,
                'following': 1,
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


class GitHubOAuthView(OAuthView):
    'github账号认证视图'
    # 在具体类中定义相应的参数
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
        return JsonResponse(msg="success!")
