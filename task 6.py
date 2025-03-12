import asyncio
import asyncpg

DB_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "database": "your_database",
    "host": "localhost",
    "port": 5432
}

async def fetch_data(table_name: str):
    """Fetch all rows from a specified table in the database"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        query = f"SELECT * FROM {table_name} LIMIT 10;"
        results = await conn.fetch(query)
        await conn.close()
        return [dict(row) for row in results]

    except Exception as e:
        return {"error": str(e)}
    async def main():
    table = input("Enter table name: ")  
    data = await fetch_data(table)
    print(data)  

if __name__ == "__main__":
    asyncio.run(main())

