# base_django_dev_scaffold
django基础服务开发脚手架 ，此项目部分代码来自其他开源项目。

基本功能
- [x] **Simple UI Admin**
- [x] **自定义认证**
- [x] **自定义全局异常**
- [x] **自定义全响应**
- [x] **自定义全局分页**
- [x] **接口版本管理**
- [x] **自定义日志输出**
  - [ ] **日志输出到DB**
- [ ] **限流**
- [ ] **权限**
- [x] **缓存**
- [x] **集成任务调度模块Celery**
- [ ] **动态添加定时任务**
- [ ] **集成第三方登录：Github/钉钉**
  - [ ] **飞书/QQ/微信/微博/百度...**




1、启动Django项目
```shell
# 1. 复制base_django_dev_scaffold/settings 目录下 prod.py 到当前目录下，修改名称为 dev.py，并修改文件内的数据等参数。

# 在项目根目录下执行
python manage.py runserver
```


2、启动 Celery 

```shell
# 在项目根目录下执行
# windows 下指定 -P eventlet
celery -A base_django_dev_scaffold worker -P eventlet -l info
```

3、启动 Celery Beat 
```shell
# 在项目根目录下执行
celery -A base_django_dev_scaffold beat -l info
```
