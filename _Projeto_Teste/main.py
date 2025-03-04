from fastapi import FastAPI
import pyodbc

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/db")
def read_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=sqlserver;'
                          'DATABASE=ChatGPTDB;'
                          'UID=sa;'
                          'PWD=Your_password123')
    cursor = conn.cursor()
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    return {"version": row[0]}

@app.get("/segmento")
def read_segmento():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=sqlserver;'
                          'DATABASE=ChatGPTDB;'
                          'UID=sa;'
                          'PWD=Your_password123')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.SegmentoClassificacao")
    rows = cursor.fetchall()
    result = [{"SegmentoID": row[0], "Nome": row[1]} for row in rows]
    return {"segmentos": result}