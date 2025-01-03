import bcrypt
from fastapi import APIRouter, HTTPException, Request
from starlette import status
from utils.Exceptions import *
from pydantic import BaseModel
from utils.error_codes import responses
from utils.logger.logger import logging
from utils.error_messages import ERROR_DETAILS
from business_layer.user import User
from business_layer.authentication import Authentication

router = APIRouter(tags=['user'])


class PasswordChangeModel(BaseModel):
    entered_password: str


class MudraPinModel(BaseModel):
    entered_mudra_pin: int


@router.get('/contacts/{contact_name}/exists',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def check_if_contact_exists(request: Request,
                                  contact_name: str
                                  ):
    try:
        result = Authentication.check_if_user_exists(contact_name)
        if not result:
            return False
        return True
    except InvalidDateException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS['invalid_month_year'])
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except UserNotFoundException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ERROR_DETAILS[404]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.get('/details',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_user_details(request: Request,
                           ):
    try:
        username = request.state.username
        result = User.get_user_email_from_username(username)
        return {
            "email": result,
            "username": username
        }
    except InvalidDateException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS['invalid_month_year'])
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.post('/pin-verification',
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
                 500: responses[500]
             }
             )
async def verify_user_mudra_pin(request: Request,
                                mudra_pin_model: MudraPinModel
                                ):
    try:
        username = request.state.username
        result = Authentication.match_mudra_pin(username, int(mudra_pin_model.entered_mudra_pin))
        return result
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.post('/password-verification',
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
                 500: responses[500]
             }
             )
async def verify_user_password(request: Request,
                               password_model: PasswordChangeModel
                               ):
    try:
        username = request.state.username
        result = Authentication.match_password(username, password_model.entered_password)
        if result:
            return True
        else :
            return False
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.post('/password',
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
                 500: responses[500]
             }
             )
async def update_user_password(request: Request,
                               password_change: PasswordChangeModel
                               ):
    try:
        username = request.state.username
        entered_password = password_change.entered_password
        if not Authentication.check_password_format(entered_password):
            raise InvalidPasswordException
        print('password changing.............')
        User.change_user_password(username, entered_password)
        return {
            "username": username,
            "status": "Password changed successfully"
        }
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.post('/mudra-pin',
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
                 500: responses[500]
             }
             )
async def update_user_mudra_pin(request: Request,
                                mudra_pin_change: MudraPinModel
                                ):
    try:
        username = request.state.username
        entered_mudra_pin = mudra_pin_change.entered_mudra_pin
        if not Authentication.check_mudra_pin_format(entered_mudra_pin):
            raise InvalidMudraPinException
        User.change_user_mudra_pin(username, entered_mudra_pin)
        return {
            "username": username,
            "status": "Mudra Pin changed successfully"
        }
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err
