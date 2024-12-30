from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette import status
from fastapi import HTTPException
from tokens.tokens import get_current_user
from utils.error_messages import ERROR_DETAILS
from jose import JWTError


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        print(request.headers,'.................................................')
        if request.url.path in ['/','/auth/login', '/auth/signup','/auth/status']:
            return await call_next(request)
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ERROR_DETAILS[401]
                                )
        token = auth_header.split(' ')[1]
        # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDEyMyIsImV4cCI6MTczMzM5ODkzMX0.xlMlwO0rm2qsMl4ZRFLCupS43mIv2e0espMxpu69MXs"
        try:
            username = get_current_user(token)
            if not username:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail=ERROR_DETAILS[401]
                                    )
            request.state.username = username
            return await call_next(request)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ERROR_DETAILS[401]
                                )
        except HTTPException as err:
            raise err







