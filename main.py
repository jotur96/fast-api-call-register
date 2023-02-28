# Python
from typing import Optional
from enum import Enum

import os

import uvicorn

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI, Depends
from fastapi import Body, Query, Path

import databases
from databases import Database


DB_NAME: str = os.getenv('DB_NAME')
DB_USER: str = os.getenv('DB_USER')
DB_PASS: str = os.getenv('DB_PASS')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')

database = databases.Database(
    'postgresql://root:12345@localhost:5431/register')


async def connect_to_db():
    try:
        await database.connect()
        print("Conexión establecida")
    except Exception as e:
        print("Error connecting to database ", e)


async def disconnect_from_db():
    await database.disconnect()
    print("Conexión cerrada")


async def select_data():
    query = "SELECT * FROM tabla"
    results = await database.fetch_all(query)
    return results


app = FastAPI()


class Register(BaseModel):
    iccid: str
    origen: str
    destino: str
    type: Optional[str]
    timestamp: str
    duration: str


@app.get('/')
def home():
    return {"message": "Hello, world!"}


@app.post("/new")
async def create_register(register: Register = Body(...)):
    print(str(register))

    print("NEW")
    await connect_to_db()

    # Define la sentencia SQL para insertar un registro en la tabla
    query = "INSERT INTO log (iccid, origen, destino, type, timestamp, duration) VALUES (:iccid, :origen, :destino, :type, :timestamp, :duration)"

    # Define los valores a insertar en la tabla
    values = {
        "iccid": register.iccid,
        "origen": register.origen,
        "destino": register.destino,
        "type": register.type,
        "timestamp": register.timestamp,
        "duration": register.duration,
    }

    # Ejecuta la sentencia SQL utilizando la conexión a la base de datos
    await database.execute(query=query, values=values)

    await disconnect_from_db()

    return register


@app.get("/all")
async def getAll():

    print("GETALL")
    await connect_to_db()

    query = f"""
        SELECT 
            iccid,
            origen,
            destino,
            type,
            timestamp,
            duration
        FROM log
    """
    queryset = await database.fetch_all(query)
    res = [Register(**dict(x)) for x in queryset]

    await disconnect_from_db()

    return {'data': res}
    pass


if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8003)
        # input()
    except Exception as e:
        print("========== ERROR ===============")
        print(e)
        # input("Presione una tecla para salir")
