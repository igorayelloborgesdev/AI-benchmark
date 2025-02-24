from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Configura a string de conexão
DATABASE_URL = f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria uma sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()