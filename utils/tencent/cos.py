#!/usr/bin/env python
# -*- coding:utf-8 -*-
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
import time


def create_bucket_name(request, project_name, region='ap-nanjing'):
    bucket_name = '%s-%s-%s-%s-%s' % (
        request.tracer.user.mobile_phone, project_name, str(int(time.time())), region, settings.TENCENT_COS_APPID)
    return bucket_name


def create_bucket(bucket, region=settings.BUCKET_REGION):
    """
    创建桶
    :param bucket: 桶名称
    :param region: 区域
    :return:
    """

    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)
    client.create_bucket(
        Bucket=bucket,
        ACL="public-read"  # private  /  public-read / public-read-write
    )


def upload_file(bucket, body, key):
    secret_id = settings.TENCENT_COS_ID
    secret_key = settings.TENCENT_COS_KEY

    region = settings.BUCKET_REGION  # 替换为用户的 Region

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

    client = CosS3Client(config)
    img_url = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=body,  # 图片对象
        Key=key  # 上传到桶之后的文件名
    )

    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, settings.BUCKET_REGION, key)
