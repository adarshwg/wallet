from fastapi import HTTPException, APIRouter, Depends, Request
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from wallet import Wallet
from Exceptions import SelfTransferException, WalletEmptyException, LowBalanceException, InvalidAmountException
from routers.error_codes import responses
from routers.auth_router import get_current_user
from logger.logger import logging
router = APIRouter(
    prefix="/wallet",
    tags=['wallet']
)
oauth2_bearer = OAuth2PasswordBearer('auth/login')


@router.get("/show-wallet", status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def show_user_wallet(request: Request, token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        logging.info(f' {request.url.path} - user [{username}] ')
        user_wallet = Wallet(username)
        return user_wallet
    except HTTPException:
        logging.info(f' {request.url.path} - Invalid token ')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.get("/balance",
            status_code=status.HTTP_200_OK,
            responses={
                400: responses[400],
                401: responses[401],
                404: responses[404],
            }
            )
async def get_wallet_balance(request: Request, token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        if username is None:
            logging.info(f' {request.url.path} - '
                         f'user: [{username}] - '
                         f'Invalid Credentials')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate the credentials'
                                )
        user_wallet = Wallet(username)
        logging.info(f' {request.url.path} - user: [{username}] ')
        return user_wallet.get_balance()
    except HTTPException:
        logging.info(f' {request.url.path} - Invalid token ')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.post("/send-amount",
             status_code=status.HTTP_200_OK,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
             }
             )
async def send_amount(request: Request, token: Annotated[str, Depends(oauth2_bearer)],
                      receiver: str, amount: int,
                      category: str = 'misc'):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        new_transaction = user_wallet.send_amount(receiver, amount, category)
        logging.info(f' {request.url.path} - user: [{username}] '
                     f'- amount: [{amount}] - category:[{category}]')
        return new_transaction
    except SelfTransferException:
        logging.info(f' {request.url.path} - user:[{receiver} -'
                     f' amount:{amount} - Self Transfer Exception')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot transfer to the same account wallet!')
    except WalletEmptyException:
        logging.info(f' {request.url.path} - amount: [{amount}] - User wallet is Empty')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet is empty!'
                            )
    except LowBalanceException:
        logging.info(f' {request.url.path} - amount: [{amount}] - User wallet balance is low ')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet balance is low for the transaction')
    except InvalidAmountException:
        logging.info(f' {request.url.path} - amount: [{amount}] -'
                     f' Invalid amount entered by user')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid amount entered!'
                                   ' Please enter positive amount'
                            )
    except HTTPException:
        logging.info(f' {request.url.path} - Invalid token ')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )


@router.post("/receive-amount",
             status_code=status.HTTP_200_OK,
             responses={
                 400: responses[400],
                 401: responses[401],
                 404: responses[404],
             }
             )
async def receive_amount(request: Request, token: Annotated[str, Depends(oauth2_bearer)],
                         sender: str, amount: int,
                         category: str = 'misc'):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        new_transaction = user_wallet.receive_amount(sender, amount, category)
        logging.info(f' {request.url.path} - user: [{username}] '
                     f'- amount: [{amount}] - category:[{category}]')
        return new_transaction
    except SelfTransferException:
        logging.info(f' {request.url.path} - user:[{sender} -'
                     f' amount:{amount} - Self Transfer Exception')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot transfer to the same account wallet!')
    except InvalidAmountException:
        logging.info(f' {request.url.path} - amount: [{amount}] -'
                     f' Invalid amount entered by user')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid amount entered! Please enter positive amount'
                            )
    except HTTPException:
        logging.info(f' {request.url.path} - Invalid token ')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
