from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from typing import List
import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# Configuração do CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados
DATABASE_SERVER = os.environ.get("DATABASE_SERVER")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

engine = create_engine(f"mssql+pymssql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# # Definição do modelo de dados
# class Usuario(Base):
#     __tablename__ = "usuarios"
#     id = Column(Integer, primary_key=True)
#     nome = Column(String)
#     email = Column(String)

# # Criação das tabelas no banco de dados
# Base.metadata.create_all(engine)

# Definição da rota para obter todos os usuários
@app.get("/usuarios/")
def read_usuarios():
    return {"message": "Bem-vindo ao Simulador de Mercado Financeiro"}
    # db = SessionLocal()
    # usuarios = db.query(Usuario).all()
    # return [{"id": usuario.id, "nome": usuario.nome, "email": usuario.email} for usuario in usuarios]