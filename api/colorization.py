import requests
from flask import request

from common import check_exists, check_one_exists
from common import get_result


class Colorization:
    def __init__(self):
        api_key = request.headers.get('X-API-KEY')
        image_file = request.files.get('image_file')
        image_url = request.form.get('image_url')
        # format png ret type = 1
        check_exists(api_key, 'X-API-KEY')
        check_one_exists(image_file, 'image_file', image_url, 'image_url')

        self.headers = {'X-API-KEY': f'{api_key}'}
        form_data = {key: value for key, value in {
            'image_url': image_url,
        }.items() if value}
        form_data_base = {
            'sync': 1,
        }
        self.form_data = {**form_data, **form_data_base}
        self.files = {key: (file.filename, file.stream, file.mimetype) for key, file in {
            'image_file': image_file,
        }.items() if file}

    def create_task(self):
        print(self.headers, self.files, self.form_data)
        url = 'https://techsz.aoscdn.com/api/tasks/visual/colorization'
        response = requests.post(url, headers=self.headers, data=self.form_data, files=self.files)
        return get_result(response)
