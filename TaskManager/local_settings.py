TENCENT_SMS_APP_ID = 1400345192  # 自己应用ID
TENCENT_SMS_APP_KEY = "b46be30119f8a28fc7f8a956b66203c2"  # 自己应用Key
TENCENT_SMS_SIGN = "我就装B怎么了"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
TENCENT_SMS_TEMPLATE = {
    'login': '571053',
    'register': '571053',
}
# redis #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100, 'decode_responses': True},  # 自动解码
            # "PASSWORD": "密码",
        }
    }
}

TENCENT_COS_ID = 'AKIDLl4C9vEFgx2vd98giXAdu1wfJm29QRlw'
TENCENT_COS_KEY = 'Bk9NXnuBJGhy5ztdBcBYnpysWMUpunYB'
BUCKET_REGION = 'ap-nanjing'
TENCENT_COS_APPID = 1300971352