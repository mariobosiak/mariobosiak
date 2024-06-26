import httpx
import sqlite3
from fastapi import FastAPI
from sqlite3 import Error

app = FastAPI()

DATABASE_FILE = 'ing.db'

# kod, który pobiera dane asynch z publicznego API Rest Countries (https://restcountries.com/) i zapisuje je do bazy danych SQLite o nazwie 'ing'. Do wykonania zapytań asynch użyjemy biblioteki httpx, a do obsługi bazy danych SQLite wykorzystamy bibliotekę sqlite3 #
# Funkcja do utworzenia połączenia z bazą danych SQLite
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
        return connection
    except Error as e:
        print(e)
    return connection

# Funkcja do utworzenia tabeli w bazie danych SQLite, jeśli nie istnieje
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                capital TEXT,
                population INTEGER,
                area REAL,
                region TEXT
            )
        ''')
        connection.commit()
        print("Table 'countries' created successfully.")
    except Error as e:
        print(e)

# Funkcja do zapisania danych kraju do bd SQLite
def save_country_to_database(connection, country_data):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO countries (name, capital, population, area, region)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            country_data.get('name'),
            country_data.get('capital'),
            country_data.get('population'),
            country_data.get('area'),
            country_data.get('region')
        ))
        connection.commit()
        print("Country data saved to database.")
    except Error as e:
        print(e)

# Endpoint do pobierania info o kraju
@app.get("/country/{country_name}")
async def get_country(country_name: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://restcountries.com/v3.1/name/{country_name}")
            response.raise_for_status()
            country_data = response.json()

        # Zapisujemy dane kraju do moji bd SQLite
        connection = create_connection(DATABASE_FILE)
        if connection:
            create_table(connection)
            save_country_to_database(connection, country_data)

        return country_data

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
        raise
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)