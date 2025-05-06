from fastapi import FastAPI
from api.routes import register, login, secret

api = FastAPI()

api.include_router(register.api_router)
api.include_router(login.api_router)
api.include_router(secret.api_router)
