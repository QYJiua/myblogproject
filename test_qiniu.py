# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'Zy81HUU6w13bO8CKHNsRHBZpwfjzkMzMa8NARrka'
secret_key = 'dCsKXJXROBM-n-MGjnP8QYspWHaStbuIW0wijP4b'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'Bucket_Name'
#上传后保存的文件名
key = 'my-python-logo.png'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = './sync/bbb.jpg'
ret, info = put_file(token, key, localfile, version='v2')
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)