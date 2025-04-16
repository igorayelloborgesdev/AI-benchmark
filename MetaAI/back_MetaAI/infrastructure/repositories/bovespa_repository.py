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
            print(f"Erro ao inserir segmento econômico {e}")
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
    
    def create_setores_economicos(self, setores_economicos):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()          
        setores_economicos_tuplas = [(setor_economicos['Descritivo'],) for setor_economicos in setores_economicos]     
        try:
            cursor.executemany("INSERT INTO dbo.SetorEconomico (Descritivo) VALUES (?)", setores_economicos_tuplas)
        except Exception as e:
            print(f"Erro ao inserir Setor Economico {e}")
        conn.commit()
        conn.close()

    def get_setores_economicos(self):
        query = "SELECT ID, Descritivo FROM dbo.SetorEconomico"
        rows = self.execute_query(query)
        setores = [{"id": row[0], "descritivo": row[1]} for row in rows]
        return setores
    
    def create_sub_setores(self, sub_setores):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()          
        sub_setor_tuplas = [(sub_setor['Descritivo'],) for sub_setor in sub_setores]     
        try:
            cursor.executemany("INSERT INTO dbo.SubSetor (Descritivo) VALUES (?)", sub_setor_tuplas)
        except Exception as e:
            print(f"Erro ao inserir SubSetor {e}")
        conn.commit()
        conn.close()

    def get_sub_setores(self):
        query = "SELECT ID, Descritivo FROM dbo.SubSetor"
        rows = self.execute_query(query)
        subsetores = [{"id": row[0], "descritivo": row[1]} for row in rows]
        return subsetores
    
    def create_segmentos(self, segmentos):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()          
        segmento_tuplas = [(segmento['Descritivo'],) for segmento in segmentos]     
        try:
            cursor.executemany("INSERT INTO dbo.Segmento (Descritivo) VALUES (?)", segmento_tuplas)
        except Exception as e:
            print(f"Erro ao inserir segmento {e}")
        conn.commit()
        conn.close()

    def get_segmentos(self):
        query = "SELECT ID, Descritivo FROM dbo.Segmento"
        rows = self.execute_query(query)
        segmentos = [{"id": row[0], "descritivo": row[1]} for row in rows]
        return segmentos
    
    # Função para buscar o ID da tabela SegmentoClassificacao
    def buscar_segmento_classificacao_id(self, sigla):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM dbo.SegmentoClassificacao WHERE Sigla = ?", sigla)
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
        
    # Função para buscar o ID da tabela SetorEconomico
    def buscar_setor_economico_id(self, descritivo):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM dbo.SetorEconomico WHERE Descritivo = ?", descritivo)
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    # Função para buscar o ID da tabela Subsetor
    def buscar_subsetor_id(self, descritivo):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM dbo.Subsetor WHERE Descritivo = ?", descritivo)
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    # Função para buscar o ID da tabela Segmento
    def buscar_segmento_id(self, descritivo):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM dbo.Segmento WHERE Descritivo = ?", descritivo)
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
        
    def create_empresas(self, empresas):
        try:
            # Inserir os dados na tabela Empresa
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO dbo.Empresa (Nome, Codigo, SegmentoClassificacaoID, SetorEconomicoID, SubsetorID, SegmentoID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', [(d['Nome'], d['Codigo'], d['SegmentoClassificacaoID'], d['SetorEconomicoID'], d['SubsetorID'], d['SegmentoID']) for d in empresas])

            # Commitar as alterações
            conn.commit()
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            conn.rollback()
        finally:
            # Fechar a conexão
            conn.close()

    def get_empresa_by_codigo(self, codigo):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        query = """
            SELECT 
                e.ID,
                e.Nome,
                e.Codigo,
                sc.Sigla AS SegmentoClassificacaoSigla,
                sc.Descritivo AS SegmentoClassificacaoDescritivo,
                se.Descritivo AS SetorEconomicoDescritivo,
                s.Descritivo AS SubsetorDescritivo,
                seg.Descritivo AS SegmentoDescritivo
            FROM 
                dbo.Empresa e
            LEFT JOIN 
                dbo.SegmentoClassificacao sc ON e.SegmentoClassificacaoID = sc.ID
            INNER JOIN 
                dbo.SetorEconomico se ON e.SetorEconomicoID = se.ID
            INNER JOIN 
                dbo.Subsetor s ON e.SubsetorID = s.ID
            INNER JOIN 
                dbo.Segmento seg ON e.SegmentoID = seg.ID
            WHERE 
                e.Codigo = ?
        """
        cursor.execute(query, codigo)
        rows = cursor.fetchall()
        empresas = []
        for row in rows:
            empresa = {
                "ID": row.ID,
                "Nome": row.Nome,
                "Codigo": row.Codigo,
                "SegmentoClassificacao": {
                    "Sigla": row.SegmentoClassificacaoSigla,
                    "Descritivo": row.SegmentoClassificacaoDescritivo
                } if row.SegmentoClassificacaoSigla else None,
                "SetorEconomico": row.SetorEconomicoDescritivo,
                "Subsetor": row.SubsetorDescritivo,
                "Segmento": row.SegmentoDescritivo
            }
            empresas.append(empresa)
        conn.close()
        return empresas