import pyodbc
import os
from dotenv import load_dotenv

# Caminho relativo para o arquivo .env, começando da pasta 'core'
dotenv_path = os.path.join(os.path.dirname(__file__), '../../core/.env')

# Carregar as variáveis do arquivo .env
load_dotenv(dotenv_path=dotenv_path)

def get_db_connection():
    """Obtém uma conexão com o banco de dados SQL Server usando variáveis de ambiente."""
    connection_string = (
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
    )

    return pyodbc.connect(connection_string)
