from fastapi import FastAPI
from routers import auth_router, wallet_router, transaction_router
from fastapi_pagination import add_pagination
from middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="Wallet Application",
    description="The purpose of the application is to provide users with"
                " a platform where they can manage and track their transactions,"
                " set up their wallets, and and monitor their expenditure."
                "The project is focused on creating an application which can help the users"
                " to manage their transactions. It can help users track their wallet amount, "
                "and provide them an overview of their transactions.",
    version="1.0.0"
)
add_pagination(app)
app.add_middleware(AuthMiddleware)
app.include_router(auth_router.router, prefix='/auth')
app.include_router(wallet_router.router, prefix='/wallet')
app.include_router(transaction_router.router, prefix='/transactions')
