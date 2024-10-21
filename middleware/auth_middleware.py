from routers.tokens.tokens import get_current_user
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from utils.logger.logger import logging


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ['/auth/login', '/auth/signup']:
            response = await call_next(request)
            return response
        else:
            logging.info('authorization middleware was called!! ')
            token = request.headers.get('authorization')
            request.state.current_user_name = get_current_user(token)
            response = await call_next(request)
            return response
