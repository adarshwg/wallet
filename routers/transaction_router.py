from fastapi import APIRouter, HTTPException, Path, Depends, Request, Query
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from utils.Exceptions import *
from transaction_manager import TransactionManager
from typing import Annotated
from fastapi_pagination import Page, paginate
from utils.error_codes import responses
from routers.auth_router import get_current_user
from utils.logger.logger import logging
from datetime import datetime

SECRET_KEY = '47a7ee9ff3c784b0baca916bcc300680424467ca4a2f6f2c4ce7b692f2b25b3d'
ALGORITHM = 'HS256'

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


@router.get('/month',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_transaction_by_month(request: Request,
                                   token: Annotated[str, Depends(oauth2_bearer)],
                                   month: int = datetime.now().date().month,
                                   year: int = datetime.now().date().year
                                   ):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_transactions_by_month(month, year, username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return paginate(result)
    except InvalidDateException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid month and year entered!')
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials- Invalid token '
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.get('/show',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_n_transactions(request: Request,
                             token: Annotated[str, Depends(oauth2_bearer)],
                             mode: str = "last",
                             number: int = Query(gt=0)
                             ):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        if mode == 'last':
            result = TransactionManager.get_last_n_transactions(username, number)
        elif mode == 'top':
            result = TransactionManager.get_top_n_transactions(username, number)
        else:
            raise ValueError
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return paginate(result)
    except ValueError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid input : non numeric value entered '
                            )
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK,
                            detail='No records found!')
        logging.info(f' {request.url.path} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials - Invalid Token '
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.get('/{transaction_id}',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_transaction_by_id(request: Request,
                                token: Annotated[str, Depends(oauth2_bearer)],
                                transaction_id: int = Path(gt=0)):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        result = TransactionManager.get_transaction_by_id(transaction_id, username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return result
    except OverflowError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Requested value is too large!')
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials - Invalid Token'
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err

