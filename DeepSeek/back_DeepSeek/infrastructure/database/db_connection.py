import pyodbc
from core.config import settings

def get_db_connection():
    connection_string = (
        f"DRIVER={settings.DB_DRIVER};"
        f"SERVER={settings.DB_SERVER};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD}"
    )
    return pyodbc.connect(connection_string)