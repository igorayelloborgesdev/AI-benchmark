# main.py
from fastapi import FastAPI

app = FastAPI()

# Seus endpoints aqui
@app.get("/")
def read_root():
    return {"Hello": "World"}