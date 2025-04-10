import pyodbc
from domain.repositories.i_bovespa_repository import IBovespaRepository
from infrastructure.database.db_connection import get_db_connection
from typing import List

class BovespaRepository(IBovespaRepository):
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