from domain.repositories.i_repositorio_segmento import IRepositorioSegmento
from decouple import config
import pyodbc
from typing import List, Dict

class RepositorioSQL(IRepositorioSegmento):
    def __init__(self):
        # Lendo variáveis do arquivo .env
        driver = config("DB_DRIVER")
        server = config("DB_SERVER")
        database = config("DB_DATABASE")
        user = config("DB_USER")
        password = config("DB_PASSWORD")

        # Montando a string de conexão
        self.conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
        )

    def salvar_segmento_classificacao(self, segmentos: list):
        """
        Insere os dados na tabela SegmentoClassificacao.
        """        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for segmento in segmentos:
                cursor.execute(
                    """
                    INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo)
                    VALUES (?, ?)
                    """,
                    segmento["Sigla"],
                    segmento["Descritivo"],
                )
            conn.commit()

    def salvar_setor_economico(self, records):
        """
        Insere os registros no banco de dados SQL Server.
        """
        if not records:
            raise ValueError("Nenhum registro válido para salvar no banco.")

        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO dbo.SetorEconomico (Descritivo)
                    VALUES (?)
                    """,
                    record["Descritivo"],
                )
            conn.commit()

    def salvar_sub_setor_economico(self, records):
        """
        Insere os registros no banco de dados SQL Server.
        """
        if not records:
            raise ValueError("Nenhum registro válido para salvar no banco.")

        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO dbo.Subsetor (Descritivo)
                    VALUES (?)
                    """,
                    record["Descritivo"],
                )
            conn.commit()            

    def salvar_segmento(self, records):
        """
        Insere os registros filtrados no banco de dados SQL Server.
        """
        if not records:
            raise ValueError("Nenhum registro válido para salvar no banco.")

        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO dbo.Segmento (Descritivo)
                    VALUES (?)
                    """,
                    record["Descritivo"],
                )
            conn.commit()

    def obter_id(self, tabela, coluna, valor):
        """
        Busca o ID em uma tabela pelo valor em uma coluna.
        """        
        if not valor:
            return None
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT ID FROM dbo.{tabela} WHERE {coluna} = ?", valor)
            result = cursor.fetchone()
            return result[0] if result else None
        
    def salvar_empresa(self, records):
        """
        Insere os registros na tabela dbo.Empresa.
        """
        if not records:
            raise ValueError("Nenhum registro válido para salvar no banco.")
        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO dbo.Empresa (Nome, Codigo, SegmentoClassificacaoID, 
                                             SetorEconomicoID, SubsetorID, SegmentoID)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    record["Nome"], record["Codigo"],
                    record["SegmentoClassificacaoID"], record["SetorEconomicoID"],
                    record["SubsetorID"], record["SegmentoID"]
                )
            conn.commit()

        print("Dados inseridos com sucesso na tabela Empresa.")
        
    def get_all_segmento_classificacao(self):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Sigla, Descritivo FROM dbo.SegmentoClassificacao")
            rows = cursor.fetchall()
            # Converter para lista de dicionários
            return [{"ID": row.ID, "Sigla": row.Sigla, "Descritivo": row.Descritivo} for row in rows]

    def get_segmentos(self):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.Segmento")
            rows = cursor.fetchall()
            # Converter para lista de dicionários
            return [{"ID": row.ID, "Descritivo": row.Descritivo} for row in rows]
        

    def get_setor_economico(self):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.SetorEconomico")
            rows = cursor.fetchall()
            # Converter para lista de dicionários
            return [{"ID": row.ID, "Descritivo": row.Descritivo} for row in rows]

    def get_sub_setor(self):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.Subsetor")
            rows = cursor.fetchall()
            # Converter para lista de dicionários
            return [{"ID": row.ID, "Descritivo": row.Descritivo} for row in rows]

    def get_empresa_by_codigo(self, codigo: str) -> dict:
        """
        Retorna os dados de uma empresa específica pelo código, incluindo os detalhes das chaves estrangeiras.
        """
        query = """
        SELECT 
            e.ID AS EmpresaID,
            e.Nome,
            e.Codigo,
            sc.Sigla AS SegmentoClassificacaoSigla,
            sc.Descritivo AS SegmentoClassificacaoDescritivo,
            se.Descritivo AS SetorEconomicoDescritivo,
            ss.Descritivo AS SubsetorDescritivo,
            s.Descritivo AS SegmentoDescritivo
        FROM dbo.Empresa e
        LEFT JOIN dbo.SegmentoClassificacao sc ON e.SegmentoClassificacaoID = sc.ID
        INNER JOIN dbo.[SetorEconomico] se ON e.SetorEconomicoID = se.ID
        INNER JOIN dbo.Subsetor ss ON e.SubsetorID = ss.ID
        INNER JOIN dbo.Segmento s ON e.SegmentoID = s.ID
        WHERE e.Codigo = ?
        """
        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, codigo)
            row = cursor.fetchone()

        if not row:
            return None  # Caso não encontre a empresa com o código fornecido
        
        # Retornar os dados como um dicionário
        return {
            "EmpresaID": row.EmpresaID,
            "Nome": row.Nome,
            "Codigo": row.Codigo,
            "SegmentoClassificacaoSigla": row.SegmentoClassificacaoSigla,
            "SegmentoClassificacaoDescritivo": row.SegmentoClassificacaoDescritivo,
            "SetorEconomicoDescritivo": row.SetorEconomicoDescritivo,
            "SubsetorDescritivo": row.SubsetorDescritivo,
            "SegmentoDescritivo": row.SegmentoDescritivo,
        }        