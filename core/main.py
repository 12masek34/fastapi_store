from fastapi import FastAPI
from api.endpoint import endpoints

app = FastAPI()

app.include_router(endpoints)
