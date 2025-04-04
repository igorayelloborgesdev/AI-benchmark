from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():    
    teste = 1
    return {"Hello": "World"}
