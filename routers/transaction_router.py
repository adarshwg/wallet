from fastapi import APIRouter, HTTPException, Path, Depends
from starlette import status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from Exceptions import *
from transaction_manager import TransactionManager
from typing import Annotated
from fastapi_pagination import Page, paginate
from routers.error_codes import responses

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
async def get_current_month_transactions(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        result = TransactionManager.get_current_month_transactions(username)
        return paginate(result)
    except InvalidDateException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid month and year entered!')
    except NoRecordsException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found for the specified time!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.get('/get-by-month',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_transaction_by_month(token: Annotated[str, Depends(oauth2_bearer)],
                                   month: int,
                                   year: int
                                   ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        result = TransactionManager.get_transactions_by_month(month, year, username)
        return paginate(result)
    except InvalidDateException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid month and year entered!')
    except NoRecordsException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found for the specified time!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.get('/top-transactions/{number}',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_top_n_transactions(token: Annotated[str, Depends(oauth2_bearer)], number: int = Path(gt=0)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get('sub')
        result = TransactionManager.get_top_n_transactions(username, number)
        return paginate(result)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Please enter numbers only'
                            )
    except NoRecordsException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.get('/last-transactions/{number}',
            status_code=status.HTTP_200_OK,
            response_model=Page[dict],
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404]
            }
            )
async def get_last_n_transactions(token: Annotated[str, Depends(oauth2_bearer)], number: int = Path(gt=0)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get('sub')
        result = TransactionManager.get_last_n_transactions(username, number)
        return paginate(result)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Please enter numbers only'
                            )
    except NoRecordsException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.get('/get-transaction/{transaction_id}',
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                404: responses[404]
            }
            )
async def get_transaction_by_id(token: Annotated[str, Depends(oauth2_bearer)], transaction_id: int = Path(gt=0)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get('sub')
        result = TransactionManager.get_transaction_by_id(transaction_id, username)
        return result
    except OverflowError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Requested value is too large!')
    except NoRecordsException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No records found with this transaction ID')
