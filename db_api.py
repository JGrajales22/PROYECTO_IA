from fastapi import FastAPI
import pyodbc

app = FastAPI()

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=TU_BASE;"
    "UID=TU_USUARIO;"
    "PWD=TU_PASSWORD;"
    "TrustServerCertificate=yes;"
)

@app.get("/query")
def ejecutar_query(sql: str):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]

        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        return results

    except Exception as e:
        return {
            "error": str(e),
            "sql": sql
        }