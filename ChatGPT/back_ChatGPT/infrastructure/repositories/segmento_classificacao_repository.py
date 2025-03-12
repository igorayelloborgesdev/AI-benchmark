import pyodbc
from typing import List, Tuple, Optional
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
    
    def get_segmento_classificacao_id(self, sigla: Optional[str]) -> Optional[int]:
        """Busca o ID do SegmentoClassificacao pela Sigla."""
        if not sigla:
            return None
        query = "SELECT ID FROM dbo.SegmentoClassificacao WHERE Sigla = ?"
        return self.fetch_single_id(query, sigla)

    def get_setor_economico_id(self, descritivo: Optional[str]) -> Optional[int]:
        """Busca o ID do SetorEconomico pelo Descritivo."""
        if not descritivo:
            return None
        query = "SELECT ID FROM dbo.SetorEconomico WHERE Descritivo = ?"
        return self.fetch_single_id(query, descritivo)

    def get_subsetor_id(self, descritivo: Optional[str]) -> Optional[int]:
        """Busca o ID do Subsetor pelo Descritivo."""
        if not descritivo:
            return None
        query = "SELECT ID FROM dbo.Subsetor WHERE Descritivo = ?"
        return self.fetch_single_id(query, descritivo)

    def get_segmento_id(self, descritivo: Optional[str]) -> Optional[int]:
        """Busca o ID do Segmento pelo Descritivo."""
        if not descritivo:
            return None
        query = "SELECT ID FROM dbo.Segmento WHERE Descritivo = ?"
        return self.fetch_single_id(query, descritivo)
    
    def fetch_single_id(self, query: str, param: str) -> Optional[int]:
        """Executa uma consulta SQL e retorna um único ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (param,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    
    def insert_many_empresas(self, empresas: List[Tuple[str, str, Optional[int], int, int, int]]) -> int:        
        """Insere várias empresas no banco de dados."""
        if not empresas:
            return 0

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO dbo.Empresa (Nome, Codigo, SegmentoClassificacaoID, SetorEconomicoID, SubsetorID, SegmentoID)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(query, empresas)
        conn.commit()
        conn.close()

        return len(empresas)
    
    def get_all_segmento_classificacao(self) -> List[Tuple[int, str, str]]:
        """Busca todos os registros da tabela SegmentoClassificacao."""
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Sigla, Descritivo FROM dbo.SegmentoClassificacao"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()        
        return [
            {
                "ID": row.ID,
                "Sigla": row.Sigla,
                "Descritivo": row.Descritivo                
            }
            for row in result
        ]
    
    def get_all_setor_economico(self) -> List[Tuple[int, str]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Descritivo FROM dbo.SetorEconomico"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return [
            {
                "ID": row.ID,
                "Descritivo": row.Descritivo                
            }
            for row in result
        ]

    def get_all_subsetor(self) -> List[Tuple[int, str]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Descritivo FROM dbo.Subsetor"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return [
            {
                "ID": row.ID,
                "Descritivo": row.Descritivo                
            }
            for row in result
        ]

    def get_all_segmento(self) -> List[Tuple[int, str]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Descritivo FROM dbo.Segmento"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()        
        return [
            {
                "ID": row.ID,
                "Descritivo": row.Descritivo                
            }
            for row in result
        ]
    
    def get_empresa_by_codigo(self, codigo: Optional[str] = None) -> List[Tuple[int, str, str, str, str, str, str]]:
        """Busca empresas e permite filtragem pelo código."""

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            e.ID, 
            e.Nome, 
            e.Codigo, 
            sc.Sigla AS SegmentoClassificacao, 
            se.Descritivo AS SetorEconomico, 
            ss.Descritivo AS Subsetor, 
            s.Descritivo AS Segmento
        FROM dbo.Empresa e
        LEFT JOIN dbo.SegmentoClassificacao sc ON e.SegmentoClassificacaoID = sc.ID
        INNER JOIN dbo.SetorEconomico se ON e.SetorEconomicoID = se.ID
        INNER JOIN dbo.Subsetor ss ON e.SubsetorID = ss.ID
        INNER JOIN dbo.Segmento s ON e.SegmentoID = s.ID
        """                
        # Adiciona filtro se um código for informado
        if codigo:
            query += " WHERE e.Codigo = ?"
            cursor.execute(query, (codigo.upper(),))
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        conn.close()

        return [
            {
                "ID": row.ID,
                "Nome": row.Nome,
                "Codigo": row.Codigo,
                "SegmentoClassificacao": row.SegmentoClassificacao,
                "SetorEconomico": row.SetorEconomico,
                "Subsetor": row.Subsetor,
                "Segmento": row.Segmento
            }
            for row in result
        ]