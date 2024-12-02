import base64
import json

import oss2
import requests
from flask import request

from common import check_exists


# 定义回调参数Base64编码函数
def encode_callback(callback_params):
    cb_str = json.dumps(callback_params).strip()
    return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))


class OssImg:
    def __init__(self):
        authorization = request.headers.get('Authorization')
        self.image_file = request.files.get('image_file')
        check_exists(self.image_file, "image_file")

        self.headers = {'authorization': authorization}
        self.json = {"filenames": [f"{self.image_file.filename}"]}
        self.files = {key: (file.filename, file.stream, file.mimetype) for key, file in {
            'image_file': self.image_file,
        }.items() if file}

    def create_task(self):
        """
        创建一个阿里云Object用来占位
        :return:阿里云oss上传需要的token
        """
        print(self.headers, self.json)
        url = 'https://aw.aoscdn.com/app/picwish/authorizations/oss?product_id=482&language=zh'
        response = requests.post(url, headers=self.headers, json=self.json)
        response_json = response.json()
        print(response_json)
        if 'status' in response_json and response_json['status'] == 200:
            if 'data' in response_json:
                response_json_data = response_json['data']
                return response_json_data
            else:
                return response_json
        else:
            print(f'Error: Failed to get the result,{response.text}')

    def put_img(self, response_json_data):
        """
        将本地图片上传替换object
        :param response_json_data: 鉴权需要的token
        :return: resource id
        """
        # 创建临时token的auth对象
        access_key_id = response_json_data['credential']['access_key_id']
        access_key_secret = response_json_data['credential']['access_key_secret']
        security_token = response_json_data['credential']['security_token']
        auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
        # 创建Bucket对象
        bucket_name = response_json_data['bucket']
        endpoint = response_json_data['endpoint']
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        # 设置回调参数
        callbackUrl = response_json_data['callback']['url']
        callbackBody = response_json_data['callback']['body']
        callbackBodyType = response_json_data['callback']['type']
        callback_params = {
            "callbackUrl": callbackUrl,
            "callbackBody": callbackBody,
            "callbackBodyType": callbackBodyType
        }
        encoded_callback = encode_callback(callback_params)

        # 上传回调
        object_name = response_json_data['objects'][f'{self.image_file.filename}']
        headers = {'x-oss-callback': encoded_callback}
        result = bucket.put_object(object_name, self.image_file.read(), headers=headers)
        result_str = result.resp.read().decode('utf-8')
        response_json = json.loads(result_str)
        # 回调响应
        print(f'Callback response: {response_json}')
        return response_json
