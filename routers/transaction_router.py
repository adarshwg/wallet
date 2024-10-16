from fastapi import APIRouter, HTTPException, Path, Depends, Request
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from Exceptions import *
from transaction_manager import TransactionManager
from typing import Annotated
from fastapi_pagination import Page, paginate
from routers.error_codes import responses
from routers.auth_router import get_current_user
from logger.logger import logging

SECRET_KEY = '47a7ee9ff3c784b0baca916bcc300680424467ca4a2f6f2c4ce7b692f2b25b3d'
ALGORITHM = 'HS256'

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


@router.get('/current-month',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_current_month_transactions(request: Request,
                                         token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_current_month_transactions(username)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return paginate(result)
    except InvalidDateException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid month and year entered!')
        logging.info(f' {request.url.path} - {str(err)} - Invalid Month and date entered ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found for the specified time!')
        logging.info(f' {request.url.path} - {str(err)} - No records found ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid token ')
        raise err


@router.get('/get-by-month',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_transaction_by_month(request: Request,
                                   token: Annotated[str, Depends(oauth2_bearer)],
                                   month: int,
                                   year: int
                                   ):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_transactions_by_month(month, year, username)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return paginate(result)
    except InvalidDateException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid month and year entered!')
        logging.info(f' {request.url.path} - {str(err)} - Invalid Date Entered ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found for the specified time!')
        logging.info(f' {request.url.path} - {str(err)} - No records found ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid token ')
        raise err


@router.get('/top-transactions/{number}',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_top_n_transactions(request: Request,
                                 token: Annotated[str, Depends(oauth2_bearer)],
                                 number: int = Path(gt=0)):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_top_n_transactions(username, number)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return paginate(result)
    except ValueError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Please enter numbers only'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid input : non numeric value ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found!')
        logging.info(f' {request.url.path} - {str(err)} - No records found ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid token ')
        raise err


@router.get('/last-transactions/{number}',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404]
            }
            )
async def get_last_n_transactions(request: Request,
                                  token: Annotated[str, Depends(oauth2_bearer)],
                                  number: int = Path(gt=0)):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_last_n_transactions(username, number)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return paginate(result)
    except ValueError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Please enter numbers only'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid input : non numeric value ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found!')
        logging.info(f' {request.url.path} - {str(err)} - No records found ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid token ')
        raise err


@router.get('/get-transaction/{transaction_id}',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                404: responses[404]
            }
            )
async def get_transaction_by_id(request: Request,
                                token: Annotated[str, Depends(oauth2_bearer)],
                                transaction_id: int = Path(gt=0)):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_transaction_by_id(transaction_id, username)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return result
    except OverflowError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Requested value is too large!')
        logging.info(f' {request.url.path} - {str(err)} - Invalid input : non numeric value ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found with this transaction ID')
        logging.info(f' {request.url.path} - {str(err)} - No records found ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
        logging.info(f' {request.url.path} - {str(err)} - Invalid token ')
        raise err
