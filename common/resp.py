from fastapi.responses import JSONResponse


def json_data(code=0, message='ok', description=None, data=None):
    """ 统一返回 json 格式
    :return:
    """
    return JSONResponse(status_code=200,
                        content={'code': code, 'message': message, 'description': description, 'data': data})
