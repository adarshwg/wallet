from fastapi import FastAPI
import prod_router

app = FastAPI()
app.include_router(prod_router.router, prefix='/prod')
