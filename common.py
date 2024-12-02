from flask import abort


def check_exists(variable, name):
    if not variable:
        error_message = {'error': f'{name} must be set'}
        raise AttributeError(error_message)


def check_one_exists(one, nameo, another, names):
    if bool(one) == bool(another):
        error_message = {'error': f'You must choose only one as param from {nameo} and {names}'}
        raise AttributeError(error_message)


def get_result(response):
    response_json = response.json()
    if 'status' in response_json and response_json['status'] == 200:
        if 'data' in response_json:
            response_json_data = response_json['data']
            if 'state' in response_json_data:
                task_state = response_json_data['state']
                # task success
                if task_state == 1:
                    print(f'success: {response_json}')
                    return response_json
                elif task_state < 0:
                    # request failed
                    abort(500, description=f'Result(failed): {response_json}')
                    pass
                else:
                    # others
                    abort(500, description=f'Result(unexpected error): {response_json}')
                    pass
    else:
        # request failed
        print(f'Error: Failed to get the result,{response.text}')
