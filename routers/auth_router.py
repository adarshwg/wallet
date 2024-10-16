from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from Exceptions import UserNotFoundException, InvalidPasswordException
from pydantic import BaseModel
from authentication import Authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from user import User
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

SECRET_KEY = '47a7ee9ff3c784b0baca916bcc300680424467ca4a2f6f2c4ce7b692f2b25b3d'
ALGORITHM = 'HS256'

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, expires_delta: timedelta):
    encode = {'sub': username}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str):
    try:
        authorized = User.login(username, password)
    except UserNotFoundException:
        raise UserNotFoundException
    except InvalidPasswordException:
        raise InvalidPasswordException
    if authorized:
        user = User(username, password)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate the credentials!'
                            )


def check_username_and_password_format(username, password):
    if not Authentication.check_username_format(username) or \
            not Authentication.check_password_format(password):
        return False
    return True


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate the credentials! '
                                )
        return {'username': username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate the credentials!  '
                            )


@router.get('/status', status_code=status.HTTP_200_OK)
async def check_status():
    return {"status": "UP"}


@router.post("/signup", response_model=Token)
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    if not check_username_and_password_format(username, password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid username or password format')
    if Authentication.check_if_username_exists(username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username already exists!'
                            )
    user = User(username, password)
    token = create_access_token(user.username, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    if not check_username_and_password_format(username, password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid username or password format')
    try:
        user = authenticate_user(username, password)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with provided credentials not found! ')
    except InvalidPasswordException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid password was entered!! ')
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate the credentials!'
                            )

    token = create_access_token(user.username, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
