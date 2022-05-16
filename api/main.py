import os

import uvicorn
from fastapi import FastAPI

from app import endpoints
from models.database import create_db


app = FastAPI()

app.include_router(endpoints)

if __name__ == "__main__":
    create_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
