from fastapi import HTTPException, APIRouter, Depends, Query
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from wallet import Wallet
from Exceptions import SelfTransferException, WalletEmptyException, LowBalanceException, InvalidAmountException
from routers.error_codes import responses
from routers.auth_router import get_current_user
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
async def show_user_wallet(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        return user_wallet
    except JWTError:
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
async def get_wallet_balance(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate the credentials'
                                )
        user_wallet = Wallet(username)
        return user_wallet.get_balance()
    except JWTError:
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
async def send_amount(token: Annotated[str, Depends(oauth2_bearer)], receiver: str, amount: int,
                      category: str = 'misc'):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        print(username)
        user_wallet = Wallet(username)
        new_transaction = user_wallet.send_amount(receiver, amount, category)
        return new_transaction
    except SelfTransferException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot transfer to the same account wallet!')
    except WalletEmptyException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet is empty!'
                            )
    except LowBalanceException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User wallet balance is low for the transaction')
    except InvalidAmountException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid amount entered! Please enter positive amount'
                            )
    except JWTError:
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
async def receive_amount(token: Annotated[str, Depends(oauth2_bearer)], sender: str, amount: int,
                         category: str = 'misc'):
    try:
        username_dict = get_current_user(token)
        username = username_dict['username']
        user_wallet = Wallet(username)
        new_transaction = user_wallet.receive_amount(sender, amount, category)
        return new_transaction
    except SelfTransferException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot transfer to the same account wallet!')
    except InvalidAmountException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid amount entered! Please enter positive amount'
                            )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the credentials'
                            )
