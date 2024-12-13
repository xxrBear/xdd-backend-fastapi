from common import state
from common.resp import json_data


class ValidateError(Exception):
    """ 自定义参数异常类
    """

    def __init__(self, name: str):
        self.name = name


class RuntimeErr(Exception):
    """ 自定义运行异常类
    """

    def __init__(self, name: str):
        self.name = name


async def validate_exception_handler(exc: ValidateError):
    """
    统一处理 ValidateError 及其子类异常的方法
    """
    return json_data(code=state.REQUEST_PARAMS_ERROR, message=exc.name)


async def runtime_exception_handler(exc: RuntimeErr):
    """
    统一处理 RuntimeErr 及其子类异常的方法
    """
    return json_data(code=state.OPERATION_ERROR, message=exc.name)


def validate_request_exception(statement, message=''):
    """
    当 statement 为 True 时，抛出请求参数异常
    :param statement:
    :param message:
    :return:
    """
    if statement:
        raise ValidateError(message)
