# Python
from typing import Optional
from enum import Enum

time_limit = "1690862400000"


@app.get('/')
def home():
    return {"message": "Hello, world!"}

@add.get('/validate')
def validate():
    return time_limit
