from starlette.requests import Request

from common import state
from common.resp import json_data


class ValidateError(Exception):
    """ 统一自定义异常类
    """

    def __init__(self, name: str):
        self.name = name


async def validate_exception_handler(request: Request, exc: ValidateError):
    """
    处理 ValidateError 及其子类异常的方法
    """
    return json_data(code=state.REQUEST_PARAMS_ERROR, description=exc.name)
