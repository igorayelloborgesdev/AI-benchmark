import pyodbc
from domain.repositories.i_bovespa_repository import IBovespaRepository
from infrastructure.database.db_connection import get_db_connection

class BovespaRepository(IBovespaRepository):
    def __init__(self):
        self.conn_str = get_db_connection()            
        self.cnxn = pyodbc.connect(self.conn_str)
        self.cursor = self.cnxn.cursor()
    def create_segmentos_economicos(self, segmentos):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        segmentos_tuplas = [(segmento['Sigla'], segmento['Descritivo']) for segmento in segmentos]        
        try:
            cursor.executemany("INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo) VALUES (?, ?)", segmentos_tuplas)
        except Exception as e:
            print(f"Erro ao inserir segmento {e}")
        conn.commit()
        conn.close()

    def get_segmentos_classificacao(self):
        query = "SELECT ID, Sigla, Descritivo FROM dbo.SegmentoClassificacao"
        rows = self.execute_query(query)
        segmentos = [{"id": row[0], "sigla": row[1], "descritivo": row[2]} for row in rows]
        return segmentos

    def execute_query(self, query):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows