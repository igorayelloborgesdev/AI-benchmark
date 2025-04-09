import pyodbc
from domain.repositories.i_bovespa_repository import IBovespaRepository
from infrastructure.database.db_connection import get_db_connection
from typing import List

class BovespaRepository(IBovespaRepository):
    def create_segmentos_economicos(self, sigla, descritivo):
        cnxn = None  # Inicializa cnxn com None
        try:            
            # conn_str = get_db_connection()
            conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=sqlserver;DATABASE=GeminiDB;UID=sa;PWD=Your_password123;Timeout=30'
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()

            insert_sql = """
            INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo)
            VALUES (?, ?);
            """
            cursor.execute(insert_sql, (sigla, descritivo))
            cnxn.commit()
            print(f"Registro inserido: Sigla={sigla}, Descritivo={descritivo}")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir dados: {sqlstate}")
            print(ex)

        finally:
            if cnxn:
                cnxn.close()
