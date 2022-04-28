from fastapi import FastAPI
from endpoints.endpoint import endpoints
import uvicorn

app = FastAPI()

app.include_router(endpoints)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
