from fastapi import HTTPException, APIRouter, Request
from starlette import status
from business_layer.wallet import Wallet
from utils.Exceptions import UserNotFoundException, SelfTransferException, WalletEmptyException, LowBalanceException, \
    InvalidAmountException, \
    DatabaseException
from utils.error_codes import responses
from utils.logger.logger import logging
from business_layer.authentication import Authentication
from business_layer.transaction import Transaction
from utils.error_messages import ERROR_DETAILS
from business_layer.otp_generator import send_otp
from business_layer.user import User

router = APIRouter(tags=['otp'])


@router.get("/", status_code=status.HTTP_200_OK,
            responses={
                404: responses[404],
                500: responses[500]
            }
            )
async def generate_otp():
    try:
        print('sending email ')
        return send_otp('adarshsingh9306@gmail.com')
    except UserNotFoundException:
        print('not sending email ')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ERROR_DETAILS['receiver_not_found'])
