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
        
    def insert_many_setor_economico(self, data: List[str]) -> int:        
        """Insere múltiplos registros na tabela SetorEconomico."""
        if not data:
            return 0  # Nenhum dado para inserir

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO dbo.[SetorEconomico] (Descritivo) VALUES (?)"
        cursor.executemany(query, [(d,) for d in data])

        conn.commit()
        cursor.close()
        conn.close()

        return len(data)  # Retorna o número de registros inseridos
    
    def insert_many_subsetor(self, data: List[str]) -> int:        
        """Insere múltiplos registros na tabela SetorEconomico."""
        if not data:
            return 0  # Nenhum dado para inserir

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO dbo.Subsetor (Descritivo) VALUES (?)"
        cursor.executemany(query, [(d,) for d in data])

        conn.commit()
        cursor.close()
        conn.close()

        return len(data)  # Retorna o número de registros inseridos
    
    def insert_many_segmento_economico(self, data: List[str]) -> int:        
        """Insere múltiplos registros na tabela SetorEconomico."""
        if not data:
            return 0  # Nenhum dado para inserir

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO dbo.Segmento (Descritivo) VALUES (?)"
        cursor.executemany(query, [(d,) for d in data])

        conn.commit()
        cursor.close()
        conn.close()

        return len(data)  # Retorna o número de registros inseridos
