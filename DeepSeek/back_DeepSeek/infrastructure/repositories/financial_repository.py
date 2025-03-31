from domain.repositories.i_financial_repository import IFinancialRepository
from infrastructure.database.db_connection import get_db_connection
from typing import List
from typing import Optional
from datetime import date

class FinancialRepository(IFinancialRepository):
    def create_cdis(self, cdis: List[any]) -> int:        
        conn = get_db_connection()        
        cursor = conn.cursor()                
        try:
            # Query para inserção em lote
            query = """
            MERGE INTO CDI_Diario AS target
            USING (VALUES (?, ?)) AS source (Data, Valor)
            ON target.Data = source.Data
            WHEN NOT MATCHED THEN
                INSERT (Data, Valor) VALUES (source.Data, source.Valor);
            """            
            params = [(cdi["data"], cdi["valor"]) for cdi in cdis]            
            cursor.executemany(query, params)            
            conn.commit()            
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao inserir CDIs: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def get_cdis_by_date_range(
        self,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None
    ):
        conn = get_db_connection()        
        cursor = conn.cursor()
        
        try:
            query = "SELECT Data, Valor FROM CDI_Diario WHERE 1=1"
            params = []
            
            # Adicionar filtros conforme os parâmetros fornecidos
            if data_inicial:
                query += " AND Data >= ?"
                params.append(data_inicial)
            if data_final:
                query += " AND Data <= ?"
                params.append(data_final)
                
            query += " ORDER BY Data DESC"
            
            cursor.execute(query, params)
            
            # Transforma cada linha em um dicionário
            return [
                {
                    "data": row.Data,
                    "valor": float(row.Valor)
                }
                for row in cursor.fetchall()
            ]

        finally:
            cursor.close()
            conn.close()

    def save_historical_data(self, data: List[any]) -> int:
        conn = get_db_connection()        
        cursor = conn.cursor()
        
        try:
            query = """
            MERGE INTO IBOV_Historico AS target
            USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (Data, Abertura, Alta, Baixa, Fechamento, Volume)
            ON target.Data = source.Data
            WHEN NOT MATCHED THEN
                INSERT (Data, Abertura, Alta, Baixa, Fechamento, Volume) 
                VALUES (source.Data, source.Abertura, source.Alta, source.Baixa, source.Fechamento, source.Volume);
            """
            
            params = [
                (d["data"], d["abertura"], d["alta"], d["baixa"], d["fechamento"], d["volume"])
                for d in data
            ]
            
            cursor.executemany(query, params)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao salvar dados do IBOV: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def get_historical_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None     
    ):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Construção dinâmica da query
            query = """
            SELECT 
                Data, 
                Abertura, 
                Alta, 
                Baixa, 
                Fechamento, 
                Volume 
            FROM IBOV_Historico 
            WHERE 1=1
            """
            params = []
            
            # Adiciona filtros de data se fornecidos
            if start_date:
                query += " AND Data >= ?"
                params.append(start_date)
            if end_date:
                query += " AND Data <= ?"
                params.append(end_date)
            
            # Ordenação padrão por data decrescente
            query += " ORDER BY Data DESC"
                        
            cursor.execute(query, params)
            
            # Mapeia resultados para objetos de domínio
            return [
                    {
                        "data": row.Data.isoformat() if row.Data else None,
                        "abertura": float(row.Abertura),
                        "alta": float(row.Alta),
                        "baixa": float(row.Baixa),
                        "fechamento": float(row.Fechamento),
                        "volume": int(row.Volume)
                    }
                    for row in cursor.fetchall()
                ]
        finally:
            cursor.close()
            conn.close()

    def save_historical_data(self, data: List[any]) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            MERGE INTO Acao_Historico AS target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?)) 
            AS source (Codigo, Data, Abertura, Alta, Baixa, Fechamento, Volume)
            ON target.Codigo = source.Codigo AND target.Data = source.Data
            WHEN NOT MATCHED THEN
                INSERT (Codigo, Data, Abertura, Alta, Baixa, Fechamento, Volume)
                VALUES (source.Codigo, source.Data, source.Abertura, source.Alta, source.Baixa, 
                        source.Fechamento, source.Volume);
            """
            
            params = [
                (
                    d["codigo"], d["data"], d["abertura"], d["alta"], 
                    d["baixa"], d["fechamento"], d["volume"]
                )
                for d in data
            ]
            
            cursor.executemany(query, params)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao salvar dados da ação: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def get_historical_data_stock(self,
        codigo: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT 
                Data, 
                Codigo,
                Abertura, 
                Alta, 
                Baixa, 
                Fechamento, 
                Volume 
            FROM Acao_Historico 
            WHERE 1=1
            """
            params = []
            
            # Filtros dinâmicos
            if codigo:
                query += " AND Codigo = ?"
                params.append(codigo.upper())
            if start_date:
                query += " AND Data >= ?"
                params.append(start_date)
            if end_date:
                query += " AND Data <= ?"
                params.append(end_date)
            
            query += " ORDER BY Data DESC"                        
            
            cursor.execute(query, params)
            
            return [
                    {
                        "data": row.Data,
                        "codigo": row.Codigo,
                        "abertura": row.Abertura,
                        "alta": row.Alta,
                        "baixa": row.Baixa,
                        "fechamento": row.Fechamento,
                        "volume": row.Volume    
                    }
                    for row in cursor.fetchall()
                ]
            
        finally:
            cursor.close()
            conn.close()