import base

from web import models

# 往数据库添加数据：链接数据库、操作、关闭链接
models.UserInfo.objects.create(username='tangshuo', email='tangshuo@live.com', mobile_phone='15595769530', password='12345aaa')
