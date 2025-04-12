import pyodbc
from domain.repositories.i_bovespa_repository import IBovespaRepository
from infrastructure.database.db_connection import get_db_connection
from typing import List
from datetime import datetime
from datetime import date

class BovespaRepository(IBovespaRepository):
    def __init__(self):
        self.conn_str = get_db_connection()            
        self.cnxn = pyodbc.connect(self.conn_str)
        self.cursor = self.cnxn.cursor()

    def create_segmentos_economicos(self, sigla, descritivo):
        cnxn = None  # Inicializa cnxn com None
        try:            
            conn_str = get_db_connection()            
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

    def get_all_segmentos_classifcacao(self):
        segmentos = []
        try:
            conn_str = get_db_connection()
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute("SELECT ID, Sigla, Descritivo FROM dbo.SegmentoClassificacao")
            rows = cursor.fetchall()
            for row in rows:
                segmento = {
                    "id": row.ID,
                    "sigla": row.Sigla,
                    "descritivo": row.Descritivo
                }                                    
                segmentos.append(segmento)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao acessar o banco de dados: {sqlstate}")
            # Aqui você pode implementar um tratamento de erro mais sofisticado
        finally:
            if cnxn:
                cnxn.close()
        return segmentos
    
    def create_subsetor(self, subsetores_a_inserir):
        cnxn = None  # Inicializa cnxn com None
        try:            
            conn_str = get_db_connection()            
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            for subsetor in subsetores_a_inserir:
                    cursor.execute("INSERT INTO dbo.[SubSetor] (Descritivo) VALUES (?)", subsetor)

            cnxn.commit()
            print(f"{cursor.rowcount} subsetores foram inseridos na tabela dbo.[SubSetor].")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir dados no banco de dados: {sqlstate}")
            if cnxn:
                cnxn.rollback()
        finally:
            if cnxn:
                cnxn.close()

    def get_all_subsetores(self):
        subsetores = []
        try:
            conn_str = get_db_connection()
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.Subsetor")
            rows = cursor.fetchall()
            for row in rows:
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                                    
                subsetores.append(subsetor)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao acessar o banco de dados: {sqlstate}")
            # Aqui você pode implementar um tratamento de erro mais sofisticado
        finally:
            if cnxn:
                cnxn.close()
        return subsetores
    
    def create_subsetores(self, setores_a_inserir):
        cnxn = None  # Inicializa cnxn com None
        try:            
            conn_str = get_db_connection()            
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            for setor in setores_a_inserir:
                    cursor.execute("INSERT INTO dbo.[SetorEconomico] (Descritivo) VALUES (?)", setor)

            cnxn.commit()
            print(f"{cursor.rowcount} setores econômicos foram inseridos na tabela dbo.[SetorEconomico].")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir dados no banco de dados: {sqlstate}")
            if cnxn:
                cnxn.rollback()
        finally:
            if cnxn:
                cnxn.close()

    def get_all_setores(self):
        setores = []
        try:
            conn_str = get_db_connection()
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.SetorEconomico")
            rows = cursor.fetchall()
            for row in rows:
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                                    
                setores.append(subsetor)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao acessar o banco de dados: {sqlstate}")
            # Aqui você pode implementar um tratamento de erro mais sofisticado
        finally:
            if cnxn:
                cnxn.close()
        return setores
    
    def create_segmentos(self, segmentos_a_inserir):
        cnxn = None  # Inicializa cnxn com None
        try:            
            conn_str = get_db_connection()            
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            for setor in segmentos_a_inserir:
                    cursor.execute("INSERT INTO dbo.[Segmento] (Descritivo) VALUES (?)", setor)

            cnxn.commit()
            print(f"{cursor.rowcount} setores econômicos foram inseridos na tabela dbo.[Segmento].")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir dados no banco de dados: {sqlstate}")
            if cnxn:
                cnxn.rollback()
        finally:
            if cnxn:
                cnxn.close()

    def get_all_segmentos(self):
        segmentos = []
        try:
            conn_str = get_db_connection()
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute("SELECT ID, Descritivo FROM dbo.Segmento")
            rows = cursor.fetchall()
            for row in rows:
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                                    
                segmentos.append(subsetor)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao acessar o banco de dados: {sqlstate}")
            # Aqui você pode implementar um tratamento de erro mais sofisticado
        finally:
            if cnxn:
                cnxn.close()
        return segmentos
        
    async def get_segmento_classificacao_id(self, sigla: str):
        if not sigla:
            return None
        conn_str = get_db_connection()
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute("SELECT ID FROM dbo.SegmentoClassificacao WHERE Sigla = ?", sigla)
        result = cursor.fetchone()                                    
        return result.ID
    
    async def get_setor_economico_id(self, descritivo: str):
        if not descritivo:
            return None       
        conn_str = get_db_connection()
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute("SELECT ID FROM dbo.SetorEconomico WHERE Descritivo = ?", descritivo)
        result = cursor.fetchone()        
        return result.ID

    async def get_subsetor_id(self, descritivo: str):
        if not descritivo:
            return None
        conn_str = get_db_connection()
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute("SELECT ID FROM dbo.SubSetor WHERE Descritivo = ?", descritivo)
        result = cursor.fetchone()        
        return result.ID
        
    async def get_segmento_id(self, descritivo: str):
        if not descritivo:
            return None       
        conn_str = get_db_connection()
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor() 
        cursor.execute("SELECT ID FROM dbo.Segmento WHERE Descritivo = ?", descritivo)
        result = cursor.fetchone()        
        return result.ID
    
    async def inserir_empresas(self, empresas_a_inserir):
        cnxn = None  # Inicializa cnxn com None
        try:            
            conn_str = get_db_connection()            
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            for empresa_data in empresas_a_inserir:
                segmento_classificacao_id = await self.get_segmento_classificacao_id(empresa_data["SegmentoClassificacaoSigla"])
                setor_economico_id = await self.get_setor_economico_id(empresa_data["SetorEconomicoDescritivo"])
                subsetor_id = await self.get_subsetor_id(empresa_data["SubsetorDescritivo"])
                segmento_id = await self.get_segmento_id(empresa_data["SegmentoDescritivo"])
                cursor.execute("""
                        INSERT INTO dbo.Empresa (Nome, Codigo, SegmentoClassificacaoID, SetorEconomicoID, SubsetorID, SegmentoID)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        empresa_data["Nome"],
                        empresa_data["Codigo"],
                        segmento_classificacao_id,
                        setor_economico_id,
                        subsetor_id,
                        segmento_id
                    ))

            cnxn.commit()
            print(f"{cursor.rowcount} empresas foram inseridas na tabela dbo.Empresa.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")
        finally:
            if cnxn:
                cnxn.close()

    async def get_empresa_by_id(self, empresa_id: str):
        try:
            conn_str = get_db_connection()
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor() 
            query = """
                SELECT
                    e.ID AS EmpresaID, e.Nome AS EmpresaNome, e.Codigo AS EmpresaCodigo,
                    sc.ID AS SegmentoClassificacaoID, sc.Sigla AS SegmentoClassificacaoSigla, sc.Descritivo AS SegmentoClassificacaoDescritivo,
                    se.ID AS SetorEconomicoID, se.Descritivo AS SetorEconomicoDescritivo,
                    sub.ID AS SubsetorID, sub.Descritivo AS SubsetorDescritivo,
                    seg.ID AS SegmentoID, seg.Descritivo AS SegmentoDescritivo
                FROM dbo.Empresa e
                LEFT JOIN dbo.SegmentoClassificacao sc ON e.SegmentoClassificacaoID = sc.ID
                INNER JOIN dbo.SetorEconomico se ON e.SetorEconomicoID = se.ID
                INNER JOIN dbo.Subsetor sub ON e.SubsetorID = sub.ID
                INNER JOIN dbo.Segmento seg ON e.SegmentoID = seg.ID
                WHERE e.Codigo = ?
            """
            cursor.execute(query, empresa_id)
            row = cursor.fetchone()
            if row:
                return {
                    "ID": row.EmpresaID,
                    "Nome": row.EmpresaNome,
                    "Codigo": row.EmpresaCodigo,
                    "SegmentoClassificacao": {
                        "ID": row.SegmentoClassificacaoID,
                        "Sigla": row.SegmentoClassificacaoSigla,
                        "Descritivo": row.SegmentoClassificacaoDescritivo
                    } if row.SegmentoClassificacaoID is not None else None,
                    "SetorEconomico": {
                        "ID": row.SetorEconomicoID,
                        "Descritivo": row.SetorEconomicoDescritivo
                    },
                    "Subsetor": {
                        "ID": row.SubsetorID,
                        "Descritivo": row.SubsetorDescritivo
                    },
                    "Segmento": {
                        "ID": row.SegmentoID,
                        "Descritivo": row.SegmentoDescritivo
                    }
                }
            return None
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao acessar o banco de dados: {sqlstate}")
            # Aqui você pode implementar um tratamento de erro mais sofisticado
        finally:
            if cnxn:
                cnxn.close()
    
    async def save_cdi_data(self, data: List):        
        try:                        
            for item in data:       
                data_obj = datetime.strptime(item['data'], '%d/%m/%Y').date()                         
                self.cursor.execute(
                    "INSERT INTO CDI_Diario (Data, Valor) VALUES (?, ?)",
                    data_obj, item['valor']
                )
            self.cnxn.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise Exception(f"Error saving CDI data to database: {sqlstate}")
        finally:
            if self.cnxn:
                self.cnxn.close()

    async def get_cdi_by_date_range(self, data_inicial: date, data_final: date):        
        query = """
            SELECT Data, Valor
            FROM CDI_Diario
            WHERE Data >= ? AND Data <= ?
            ORDER BY Data
        """
        self.cursor.execute(query, data_inicial, data_final)
        rows = self.cursor.fetchall()
        return [{"Data": row.Data, "Valor": row.Valor} for row in rows]
    
    async def save_ibov_data(self, data: List):
        try:
            for item in data:
                self.cursor.execute(
                    "INSERT INTO IBOV_Historico (Data, Abertura, Alta, Baixa, Fechamento, Volume) VALUES (?, ?, ?, ?, ?, ?)",
                    item['Data'], item['Abertura'], item['Alta'], item['Baixa'], item['Fechamento'], item['Volume']
                )
            self.cnxn.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise Exception(f"Error saving IBovespa data to database: {sqlstate}")
        finally:
            if self.cnxn:
                self.cnxn.close()

    async def get_ibov_by_date_range(self, data_inicial: date, data_final: date):
        query = """
            SELECT Data, Abertura, Alta, Baixa, Fechamento, Volume
            FROM IBOV_Historico
            WHERE Data >= ? AND Data <= ?
            ORDER BY Data
        """
        self.cursor.execute(query, data_inicial, data_final)
        rows = self.cursor.fetchall()
        return [
            {
                "Data": row.Data,
                "Abertura": row.Abertura,
                "Alta": row.Alta,
                "Baixa": row.Baixa,
                "Fechamento": row.Fechamento,
                "Volume": row.Volume,
            }                
            for row in rows
        ]
    
    async def save_stock_data(self, data: List):
        try:
            for item in data:
                self.cursor.execute(
                    "INSERT INTO Acao_Historico (Codigo, Data, Abertura, Alta, Baixa, Fechamento, Volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    item['codigo'], item['data'], item['abertura'], item['alta'], item['baixa'], item['fechamento'], item['volume']
                )
            self.cnxn.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise Exception(f"Error saving IBovespa data to database: {sqlstate}")
        finally:
            if self.cnxn:
                self.cnxn.close()

    def get_acao_historico(self, codigo: str, data_inicial: date, data_final: date) -> List:
        query = """
            SELECT Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume
            FROM Acao_Historico
            WHERE Codigo = ? AND Data >= ? AND Data <= ?
            ORDER BY Data
        """
        self.cursor.execute(query, codigo, data_inicial, data_final)
        rows = self.cursor.fetchall()
        return [
            {
                "Data": row.Data,
                "Codigo": row.Codigo,
                "Abertura": row.Abertura,
                "Alta": row.Alta,
                "Baixa": row.Baixa,
                "Fechamento": row.Fechamento,
                "Volume": row.Volume,
            }            
            for row in rows
        ]