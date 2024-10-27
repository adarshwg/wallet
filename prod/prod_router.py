from fastapi import APIRouter
from prod_db import get_number

router = APIRouter(tags=['prod'])


@router.get('/', status_code=200)
async def get_product(token: ):
    return get_number()
