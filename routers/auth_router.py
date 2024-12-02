from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request
from starlette import status
from utils.Exceptions import UserNotFoundException, InvalidPasswordException, DatabaseException
from pydantic import BaseModel
from business_layer.authentication import Authentication
from fastapi.security import OAuth2PasswordRequestForm
from business_layer.user import User
from datetime import timedelta
from jose import JWTError
from utils.logger.logger import logging
from utils.error_codes import responses
from tokens.tokens import create_access_token
from utils.error_messages import ERROR_DETAILS

router = APIRouter(
    tags=['auth']
)


class Token(BaseModel):
    access_token: str
    token_type: str


async def authenticate_user(username: str, password: str):
    """
    Authenticates the user using the business layer's authentication mechanism
    :param username: the unique username with which the user wants to sign in.
    :param password: the password for that username
    :return: None
    """
    try:
        authorized = Authentication.login(username, password.encode('utf-8'))
    except UserNotFoundException:
        raise UserNotFoundException
    except InvalidPasswordException:
        raise InvalidPasswordException
    except DatabaseException:
        raise DatabaseException(ERROR_DETAILS[500])
    if authorized:
        try:
            user = User(username, password)
        except DatabaseException:
            raise DatabaseException(ERROR_DETAILS[500])
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )


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
    """
    This function is used to make the user sign up to the wallet application,
    creates the user object, and simultaneously inserts the user details into the database.
    :param request:
    :param form_data:
    :return:
    """
    username = form_data.username
    password = form_data.password
    if not Authentication.check_username_and_password_format(username, password):
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=ERROR_DETAILS['invalid_credentials_format'])
        logging.info(f' {request.url.path} - {str(err)}')
        raise err
    try:
        if Authentication.check_if_username_exists(username):
            err = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=ERROR_DETAILS[409]
                                )
            logging.info(f' {request.url.path} - {str(err)}')
            raise err
        #todo here the user object is being created here which is wrong, for signup.
        user = User(username, password)
        token = create_access_token(user.username, timedelta(minutes=20))
        logging.info(f' {request.url.path} - {status.HTTP_201_CREATED} - user: - [{username}] - account created')
    except JWTError:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
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
    if not Authentication.check_username_and_password_format(username, password):
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_DETAILS['invalid_credentials_format'])
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    try:
        await authenticate_user(username, password)
        token = create_access_token(username, timedelta(minutes=20))
        logging.info(f' {request.url.path} - {status.HTTP_201_CREATED} - user : [{username}] logged in  ')
    except UserNotFoundException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS[401])
        logging.error(f' {request.url.path} - {str(err)}')
        raise err
    except InvalidPasswordException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401])
        logging.info(f' {request.url.path} - {str(err)}  ')
        raise err
    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)}',stack_info=True,stacklevel=0)

        raise err
    except JWTError:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)}')
        raise err
    return {'access_token': token, 'token_type': 'bearer'}
