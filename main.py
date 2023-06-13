# Python
from fastapi import FastAPI
from typing import Optional
from enum import Enum

time_limit = "1690862400000"


app = FastAPI()

@app.get('/')
def home():
    return {"message": "Hello, world!"}

@app.get('/validate')
def validate():
    return time_limit
