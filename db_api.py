from fastapi import FastAPI
import pyodbc

app = FastAPI()

# 🔌 CONEXIÓN SQL SERVER
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=10.29.113.5;"
    "DATABASE=BD1;"
    "UID=sa;"
    "PWD=Cubano.2019;"
    "TrustServerCertificate=yes;"
)

@app.get("/query")
def ejecutar_query(sql: str):
    cursor = conn.cursor()
    cursor.execute(sql)

    columns = [column[0] for column in cursor.description]
    results = []

    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))

    return results