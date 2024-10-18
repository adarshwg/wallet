from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request
from starlette import status
from Exceptions import UserNotFoundException, InvalidPasswordException,DatabaseException
from pydantic import BaseModel
from authentication import Authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from user import User
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from logger.logger import logging
from routers.error_codes import responses
# logging.disable()


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
    try:
        encode = {'sub': username}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise JWTError('Token encoding failed')


def authenticate_user(username: str, password: str):
    try:
        authorized = User.login(username, password)
    except UserNotFoundException:
        raise UserNotFoundException
    except InvalidPasswordException:
        raise InvalidPasswordException
    except DatabaseException:
        raise DatabaseException('Internal Server Error')
    if authorized:
        try:
            user = User(username, password)
        except DatabaseException:
            raise DatabaseException('Internal Server Error')
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


@router.post("/signup",
             response_model=Token,
             status_code=status.HTTP_201_CREATED,
             responses={
                 403: responses[403],
                 409: responses[409],
                 500: responses[500]
             }
             )
async def signup(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    if not check_username_and_password_format(username, password):
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid username or password format')
        logging.info(f' {request.url.path} - Invalid username or password format')
        raise err
    try:
        if Authentication.check_if_username_exists(username):
            err = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Username already exists!'
                                )
            logging.info(f' {request.url.path} - Username already exists')
            raise err
        user = User(username, password)
        token = create_access_token(user.username, timedelta(minutes=20))
        logging.info(f' {request.url.path} - user: - [{username}] - account created')
    except JWTError:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - Invalid Token ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - Internal Server Error ')
        raise err
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/login",
             response_model=Token,
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 403: responses[404],
                 500: responses[500]
             }
             )
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    if not check_username_and_password_format(username, password):
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid username or password format')
        logging.info(f' {request.url.path} - invalid username or password format  ')
        raise err
    try:
        user = authenticate_user(username, password)
        token = create_access_token(user.username, timedelta(minutes=20))
        logging.info(f' {request.url.path} - user : [{username}] logged in  ')
    except UserNotFoundException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with provided credentials not found! ')
        logging.info(f' {request.url.path} - user not found')
        raise err
    except InvalidPasswordException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid password was entered!! ')
        logging.info(f' {request.url.path} - Invalid password credentials entered  ')
        raise err
    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - Internal Server Error ')
        raise err
    except JWTError:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - Internal Server Error ')
        raise err
    return {'access_token': token, 'token_type': 'bearer'}
