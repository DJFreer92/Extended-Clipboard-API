from fastapi import FastAPI
from app.api.clipboard import clipboard_endpoints

app: FastAPI = FastAPI()

app.include_router(clipboard_endpoints.router)
