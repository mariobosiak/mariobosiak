from fastapi import FastAPI, HTTPException
from sqlite3 import Error
import aiohttp
import asyncio
import sqlite3

app = FastAPI()

DATABASE_FILE = 'ing.db'

async def pobierz_dane_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Błąd podczas pobierania danych")
            return await response.json()

@app.get("/dane/")
async def pobierz_dane(url: str):
    try:
        dane = await pobierz_dane_async(url)
        return dane
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
