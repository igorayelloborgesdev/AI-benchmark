import pyodbc
from typing import List, Tuple
from domain.repositories.i_segmento_classificacao_repository import ISegmentoClassificacaoRepository
from infrastructure.database.database import get_db_connection

class SegmentoClassificacaoRepository(ISegmentoClassificacaoRepository):
    """Implementação do repositório para inserir dados na tabela SegmentoClassificacao."""

    def insert_many(self, data: List[Tuple[str, str]]) -> int:
        """Insere múltiplos registros no banco de dados SQL Server."""
        if not data:
            return 0
        conn = get_db_connection()            
        cursor = conn.cursor()
        query = "INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo) VALUES (?, ?)"
        cursor.executemany(query, data)
        conn.commit()
        conn.close()
        return len(data)
