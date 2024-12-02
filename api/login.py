import requests
from flask import request

from common import check_exists


class Login:
    def __init__(self):

        telephone = request.form.get("telephone")
        password = request.form.get("password")
        check_exists(telephone, "telephone")
        check_exists(password, "password")

        self.json = {
            'telephone': telephone,
            'password': password,
            'language': 'zh',
            'country_code': "+86",
            'product_id': "482",
        }

    def create_task(self):
        print(self.json)
        url = 'https://aw.aoscdn.com/base/passport/v2/login/telephone'
        response = requests.post(url, json=self.json)
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
