from starlette.middleware.base import BaseHTTPMiddleware

from common import state
from common.resp import json_data

OPEN_URL = ['/docs', '/openapi.json', '/redoc']
SKIP_URL = ['/api/user/register', '/api/user/login', '/', '/api/user/get/login', '/api/question/ai_generate/sse']
ADMIN_URL = []


class UserLoginStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """
        中间件统一检查用户需要用户登录的请求
        :param request:
        :param call_next:
        :return:
        """
        request_path = request.url.path
        if request_path not in OPEN_URL + SKIP_URL:
            user_login_state = request.session.get('user_login_state')
            if not user_login_state:
                return json_data(**{'code': state.USER_NOT_LOGIN, 'message': '用户未登录'})
        response = await call_next(request)
        return response


class CheckAdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """
        中间件统一检查管理员请求
        :param request:
        :param call_next:
        :return:
        """
        request_path = request.url.path
        if request_path in ADMIN_URL:
            user_login_state = request.session.get('user_login_state')
            user_role = user_login_state.get('user_role')
            if user_role != 'admin':
                return json_data(**{'code': state.NO_AUTH_ERROR, 'message': '用户无权限'})
        response = await call_next(request)
        return response
