from typing import Annotated
from fastapi import HTTPException, Depends
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

SECRET_KEY = '47a7ee9ff3c784b0baca916bcc300680424467ca4a2f6f2c4ce7b692f2b25b3d'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


def create_access_token(username: str, expires_delta: timedelta):
    try:
        encode = {'sub': username}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise JWTError('Token encoding failed')


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate the credentials! '
                                )
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate the credentials!  '
                            )
