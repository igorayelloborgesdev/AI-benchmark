from pathlib import Path
import os
from dotenv import load_dotenv

# Define o caminho para o arquivo .env no subdiretório core
dotenv_path = Path('./core/.env')
loaded = load_dotenv(dotenv_path=dotenv_path, verbose=True)
print(f"load_dotenv() retornou: {loaded}")

class Settings:
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

settings = Settings()
