import base
import uuid
import datetime
from web import models

# 往数据库添加数据：链接数据库、操作、关闭链接
# models.UserInfo.objects.create(username='tangshuo', email='tangshuo@live.com', mobile_phone='15595769530', password='12345aaa')
policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()

models.Transaction.objects.create(
    status=2,
    order=str(uuid.uuid4()),
    user=models.UserInfo.objects.filter(username='tangshuo').first(),
    price_policy=policy_object,
    count=0,
    price=0,
    start_datetime=datetime.datetime.now(),
)
