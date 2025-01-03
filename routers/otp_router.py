from fastapi import HTTPException, APIRouter, Request
from starlette import status
from business_layer.wallet import Wallet
from utils.Exceptions import UserNotFoundException, SelfTransferException, WalletEmptyException, LowBalanceException, \
    InvalidAmountException, \
    DatabaseException
from utils.error_codes import responses
from utils.error_messages import ERROR_DETAILS
from business_layer.otp_generator import send_otp, match_otp
from pydantic import BaseModel

router = APIRouter(tags=['otp'])


class OTPValidatorModel(BaseModel):
    entered_otp: str
    hashed_otp: str


@router.get("/",
            )
async def generate_otp():
    try:
        print('sending email ')
        generated_otp = send_otp('adarshsingh9306@gmail.com')
        return generated_otp
    except UserNotFoundException:
        print('not sending email ')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ERROR_DETAILS['receiver_not_found'])


@router.post("/verify", )
async def verify_otp(otp_model: OTPValidatorModel):
    print("otp verification ",otp_model)
    result = match_otp(otp_model.entered_otp, otp_model.hashed_otp)
    print("otp verification status is : ")
    return {
        "status": "success" if result else "failure"
    }
