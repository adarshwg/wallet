from fastapi import APIRouter, HTTPException, Path, Request, Query
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from utils.Exceptions import *
from business_layer.transaction_manager import TransactionManager
from fastapi_pagination import Page, paginate
from utils.error_codes import responses
from utils.logger.logger import logging
from datetime import datetime
from utils.error_messages import ERROR_DETAILS

router = APIRouter(
    tags=['transactions']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_transaction_dictionary(transaction):
    time_parser = ''
    if transaction['hours'] < 12:
        time_parser = "a.m."
    else:
        if transaction['hours'] > 12:
            transaction['hours'] -= 12
        time_parser = "p.m."
    return {
        "Transaction ID ": transaction.get("transaction_id"),
        "Amount ": transaction.get("amount"),
        "Sender ": transaction.get("sender"),
        "Receiver ": transaction.get("receiver"),
        "Time ": f'{transaction.get("hours")}:{transaction.get("minutes")} {time_parser}',
        "Date ": f'{transaction.get("day")}/{transaction.get("month")}/{transaction.get("year")}',
        "Category ": transaction.get("category")
    }


@router.get('/recent-contacts',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_top_ten_recent_contacts(request: Request):
    try:
        username = request.state.username
        result = TransactionManager.get_top_ten_recent_contacts(username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return result[::-1]
    except OverflowError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS['value_overflow'])
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


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
                                   month: int = datetime.now().date().month,
                                   year: int = datetime.now().date().year
                                   ):
    try:
        username = request.state.username
        result = TransactionManager.get_transactions_by_month(month, year, username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return paginate(result)
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
                             mode: str = "last",
                             number: int = Query(gt=0)
                             ):
    try:
        username = request.state.username
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
                            detail=ERROR_DETAILS['invalid_int_input']
                            )
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK,
                            detail=ERROR_DETAILS['no_records'])
        logging.info(f' {request.url.path} ')
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


@router.get('/contact/{contact_name}',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
                500: responses[500]
            }
            )
async def get_transactions_for_contact(request: Request,
                                       contact_name: str):
    try:
        username = request.state.username
        result = TransactionManager.get_all_transactions_for_contact(username, contact_name)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return result
    except OverflowError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS['value_overflow'])
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')


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
                                transaction_id: int = Path(gt=0)):
    try:
        username = request.state.username
        result = TransactionManager.get_transaction_by_id(transaction_id, username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return get_transaction_dictionary(result)
    except OverflowError:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ERROR_DETAILS['value_overflow'])
        logging.warning(f' {request.url.path} - {str(err)} ')
        raise err
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401]
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except NoRecordsException:
        err = HTTPException(status_code=status.HTTP_200_OK)
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err