import time

import requests
from flask import request

from common import check_exists


class FaceCutout:
    def __init__(self):
        authorization = request.headers.get("authorization")
        resource_id = request.form.get("resource_id")
        check_exists(authorization, "authorization")
        check_exists(resource_id, "resource_id")
        self.headers = {
            "authorization": authorization,
        }
        self.json = {
            'source_resource_id': resource_id,
            "language": "zh",
            "product_id": 482,
        }

    def create_task(self):
        print(self.json)
        url = 'https://aw.aoscdn.com/app/picwish/tasks/login/face-cutout?product_id=482&language=zh'
        response = requests.post(url, headers=self.headers, json=self.json)
        task_id = None
        response_json = response.json()
        if 'status' in response_json and response_json['status'] == 200:
            result_tag = 'failed'
            if 'data' in response_json:
                response_json_data = response_json['data']
                if 'task_id' in response_json_data:
                    result_tag = 'successful'
                    task_id = response_json_data['task_id']
            print(f'Result of created task({result_tag}): {response_json}')
        else:
            raise Exception(f'Failed to create task,{response.text}')
        return task_id

    def polling_task_result(self, task_id, time_out=300):
        url = f'https://aw.aoscdn.com/app/picwish/tasks/login/face-cutout/{task_id}?product_id=482&language=zh'
        for i in range(time_out):
            if i != 0:
                time.sleep(1)
            response = requests.get(url, headers=self.headers)
            response_json = response.json()
            if 'status' in response_json and response_json['status'] == 200:
                if 'data' in response_json:
                    response_json_data = response_json['data']
                    if 'state' in response_json_data:
                        task_state = response_json_data['state']
                        if task_state == 1:
                            print(f'Result(successful): {response_json}')
                            return response_json
                        elif task_state < 0:
                            raise Exception(f'Result(failed): {response_json}')
                print(f'Result(polling): {response_json}')
                if i == time_out - 1:
                    raise Exception('Timeout while polling.')
            else:
                raise Exception(f'Error: Failed to get the task\'s result,{response.text}')
