from fastapi import HTTPException, APIRouter, Request
from starlette import status
from business_layer.wallet import Wallet
from utils.Exceptions import SelfTransferException, WalletEmptyException, LowBalanceException, InvalidAmountException, \
    DatabaseException
from utils.error_codes import responses
from utils.logger.logger import logging
from business_layer.authentication import Authentication
from business_layer.transaction import Transaction
from utils.error_messages import ERROR_DETAILS
from pydantic import BaseModel

router = APIRouter(tags=['wallet'])


class SendAmountRequest(BaseModel):
    receiver: str
    amount: int
    mudra_pin: int
    category: str = 'misc'


def transaction_dictionary(transaction: Transaction, wallet: Wallet):
    return {
        "amountSent": transaction.amount,
        "receiver": transaction.receiver,
        "date": f'{transaction.day}/{transaction.month}/{transaction.year}',
        "time": f'{transaction.hours} : {transaction.minutes}',
        "category": transaction.category,
        "transactionId": transaction.transaction_id,
        "remainingBalance": wallet.get_balance()
    }


def create_wallet_from_username(username):
    return Wallet(username)


@router.get("/", status_code=status.HTTP_200_OK,
            responses={
                401: responses[401],
                500: responses[500]
            }
            )
async def show_user_wallet(request: Request):
    try:
        username = request.state.username
        user_wallet = create_wallet_from_username(username)
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user [{username}] ')
        return user_wallet
    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err
    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500])
        logging.error(f' {request.url.path} - {str(err)}')
        raise err


@router.get("/balance",
            status_code=status.HTTP_200_OK,
            responses={
                401: responses[401],
                500: responses[500]
            }
            )
async def get_wallet_balance(request: Request):
    try:
        username = request.state.username
        if username is None:
            err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ERROR_DETAILS[401]
                                )
            logging.info(f' {request.url.path} - {str(err)}')
            raise err
        user_wallet = create_wallet_from_username(username)
        balance = user_wallet.get_balance()
        logging.info(f' {request.url.path} - {status.HTTP_200_OK} - user: [{username}] ')
        return balance
    except HTTPException:
        err = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ERROR_DETAILS[401])
        logging.info(f' {request.url.path} - {str(err)}')
        raise err

    except DatabaseException:

        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ERROR_DETAILS[500]
                            )
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err


@router.post(
    "/payment",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: responses[400],
        401: responses[401],
        403: responses[404],
        500: responses[500],
    },
)
async def send_amount(
        request: Request,
        send_request: SendAmountRequest
):
    try:
        username = request.state.username
        print(send_request)
        # Extract data from the request model
        receiver = send_request.receiver
        amount = send_request.amount
        entered_mudra_pin = send_request.mudra_pin
        category = send_request.category

        user_wallet = create_wallet_from_username(username)

        # Check if the receiver exists
        if not Authentication.check_if_user_exists(receiver):
            print('user does not exist!!!!!!1')
            err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_DETAILS['receiver_not_found'])
            logging.info(f' {request.url.path} - {str(err)} ')
            raise err

        receiver_wallet = create_wallet_from_username(receiver)
        new_transaction = user_wallet.send_amount(receiver, amount, entered_mudra_pin, category)
        receiver_wallet.receive_amount(username, amount)

        logging.info(f' {request.url.path} - {status.HTTP_201_CREATED} - user: [{username}] '
                     f'- amount: [{amount}] - category:[{category}]')
        return transaction_dictionary(new_transaction, user_wallet)

    except SelfTransferException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_DETAILS['self_transfer'])
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err

    except WalletEmptyException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_DETAILS['wallet_empty'])
        logging.info(f' {request.url.path} - {str(err)}')
        raise err

    except LowBalanceException:
        err = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_DETAILS['low_user_balance'])
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err

    except InvalidAmountException:
        err = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_DETAILS['invalid_amount'])
        logging.info(f' {request.url.path} - {str(err)}')
        raise err

    except HTTPException as err:
        logging.info(f' {request.url.path} - {str(err)} ')
        raise err

    except DatabaseException:
        err = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ERROR_DETAILS[500])
        logging.error(f' {request.url.path} - {str(err)} ')
        raise err
