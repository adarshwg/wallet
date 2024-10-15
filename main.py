from fastapi import FastAPI
from starlette import status
from routers import auth_router,wallet_router,transaction_router
from fastapi_pagination import Page, add_pagination, paginate
app = FastAPI()
add_pagination(app)
app.include_router(auth_router.router)
app.include_router(wallet_router.router)
app.include_router(transaction_router.router)

