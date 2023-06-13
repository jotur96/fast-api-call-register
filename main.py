# Python
from fastapi import FastAPI
from typing import Optional
from enum import Enum
import uvicorn

time_limit = "1690862400000"


app = FastAPI()

@app.get('/')
def home():
    return {"message": "Hello, world!"}

@app.get('/validate')
def validate():
    return time_limit



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)