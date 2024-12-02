from flask import Flask, jsonify

from api.colorization import Colorization
from api.face_cutout import FaceCutout
from api.login import Login
from api.oss_img import OssImg

app = Flask(__name__)


@app.route('/picwish/login', methods=['POST'])
def picwish_login():
    try:
        result = Login().create_task()
        result_select = {'api_token': f'Bearer {result["api_token"]}'}
        return jsonify(result_select)
    except AttributeError as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 400
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 500


@app.route('/picwish/oss-img', methods=['POST'])
def picwish_oss_img():
    try:
        token = OssImg().create_task()
        result = OssImg().put_img(token)
        result_select = {'resource_id': result['data']['resource_id']}
        return jsonify(result_select)
    except AttributeError as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 400
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 500


@app.route('/picwish/face-cutout', methods=['POST'])
def picwish_face_cutout():
    try:
        task_id = FaceCutout().create_task()
        if task_id is None:
            raise Exception('Failed to create task,task id is None.')
        result = FaceCutout().polling_task_result(task_id)
        result_select = {'image': result['data']['image']}
        return jsonify(result_select)
    except AttributeError as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 400
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 500


@app.route('/picwish/colorization', methods=['POST'])
def picwish_colorization():
    try:
        result = Colorization().create_task()
        result_select = {'image': result['data']['image']}
        return jsonify(result_select)
    except AttributeError as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 400
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify(error_message), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
