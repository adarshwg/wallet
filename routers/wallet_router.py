from fastapi import HTTPException, APIRouter, Depends, Request
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from wallet import Wallet
from Exceptions import SelfTransferException, WalletEmptyException, LowBalanceException, InvalidAmountException, \
    DatabaseException
from routers.error_codes import responses
from routers.auth_router import get_current_user
from logger.logger import logging
from authentication import Authentication

router = APIRouter(
    prefix="/wallet",
    tags=['wallet']
)
oauth2_bearer = OAuth2PasswordBearer('auth/login')


@router.get("/show-wallet", status_code=status.HTTP_200_OK,
            responses={
                401: responses[401],
                500: responses[500]
            }
            )
async def show_user_wallet(request: Request, token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user [{username}] ')
        return user_wallet
    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error')
        logging.info(f' {request.url.path} - {str(err)}')
        raise err


@router.get("/balance",
            status_code=status.HTTP_200_OK,
            responses={
                401: responses[401],
                500: responses[500]
            }
            )
async def get_wallet_balance(request: Request, token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        if username is None:
            err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate the credentials'
                                )
            logging.info(f' {request.url.path} - {str(err)}')
            raise err
        user_wallet = Wallet(username)
        balance = user_wallet.get_balance()
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return balance
    except HTTPException as err:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials')
        logging.info(f' {request.url.path} - {str(err)}')
        raise err

    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err

@router.post("/send-amount",
             status_code=status.HTTP_201_CREATED,
             responses={
                 400: responses[400],
                 401: responses[401],
                 403: responses[404],
                 500: responses[500]
             }
             )
async def send_amount(request: Request,
                      token: Annotated[str, Depends(oauth2_bearer)],
                      receiver: str, amount: int,
                      category: str = 'misc'):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        if not Authentication.check_if_username_exists(receiver):
            err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Receiver does not exist')
            logging.info(f' {request.url.path} - {str(err)} ')
            raise err
        receiver_wallet = Wallet(receiver)
        new_transaction = user_wallet.send_amount(receiver, amount, category)
        receiver_wallet.receive_amount(username, amount)
        logging.info(f' {request.url.path} - {status.HTTP_201_CREATED} - user: [{username}] '
                     f'- amount: [{amount}] - category:[{category}]')
        return new_transaction
    except SelfTransferException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot transfer to the same account wallet!')
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err

    except WalletEmptyException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet is empty!'
                            )
        logging.info(f' {request.url.path} - {str(err)}')
        raise err
    except LowBalanceException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet balance is low for the transaction')
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except InvalidAmountException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid amount entered!'
                                   ' Please enter positive amount'
                            )
        logging.info(f' {request.url.path} - {str(err)}')
        raise err
    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal Server Error'
                            )
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
