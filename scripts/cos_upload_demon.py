from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


secret_id = 'AKIDLl4C9vEFgx2vd98giXAdu1wfJm29QRlw'  # 替换为用户的 secretId

secret_key = 'Bk9NXnuBJGhy5ztdBcBYnpysWMUpunYB'  # 替换为用户的 secretKey

region = 'ap-nanjing'  # 替换为用户的 Region  ap-nanjing

token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
response = client.upload_file(
    Bucket='task-manager-1300971352',
    LocalFilePath='base.py',  # 本地文件的路径
    Key='base.py',  # 上传到桶之后的文件名
    PartSize=1,
    MAXThread=10,
    EnableMD5=False
)
print(response['ETag'])
