from fastapi import HTTPException, APIRouter, Request
from starlette import status
from business_layer.wallet import Wallet
from utils.Exceptions import UserNotFoundException, SelfTransferException, WalletEmptyException, LowBalanceException, \
    InvalidAmountException, \
    DatabaseException
from utils.error_codes import responses
from utils.error_messages import ERROR_DETAILS
from business_layer.otp_generator import send_otp

router = APIRouter(tags=['otp'])


@router.get("/",
            )
async def generate_otp():
    try:
        print('sending email ')
        return send_otp('adarshsingh9306@gmail.com')
    except UserNotFoundException:
        print('not sending email ')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ERROR_DETAILS['receiver_not_found'])
