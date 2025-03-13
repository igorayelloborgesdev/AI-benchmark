from datetime import datetime
from typing import List, Tuple, Optional
from domain.repositories.i_finance_repository import IFinanceRepository
from infrastructure.database.database import get_db_connection

class FinanceRepository(IFinanceRepository):
    """Repositório para salvar os dados do CDI diário no banco de dados."""

    def insert_cdi_data(self, data: List[Tuple[str, float]]) -> int:
        """Insere múltiplos registros na tabela CDI_Diario."""
        if not data:
            return 0        
        conn = get_db_connection()
        cursor = conn.cursor()

         # Converter datas e remover duplicatas
        data_converted = list({
            (datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d"), v)
            for d, v in data
        })
        
        query = "INSERT INTO dbo.CDI_Diario (Data, Valor) VALUES (?, ?)"
        cursor.executemany(query, data_converted)
        
        conn.commit()
        cursor.close()
        conn.close()

        return len(data_converted)
    
    def get_cdi_data(self, data_inicial: Optional[str], data_final: Optional[str]) -> List[Tuple[str, float]]:
        """
        Busca os dados do CDI filtrando por data inicial e final.

        :param data_inicial: Data inicial no formato 'yyyy-MM-dd' (opcional).
        :param data_final: Data final no formato 'yyyy-MM-dd' (opcional).
        :return: Lista de tuplas [(Data, Valor)].
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Montar a query com filtros opcionais
        query = "SELECT Data, Valor FROM CDI_Diario WHERE 1=1"
        params = []

        if data_inicial:
            query += " AND Data >= ?"
            params.append(data_inicial)

        if data_final:
            query += " AND Data <= ?"
            params.append(data_final)

        query += " ORDER BY Data"

        cursor.execute(query, params)
        result = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return [(row.Data.strftime("%Y-%m-%d"), row.Valor) for row in result]
    
    def insert_ibov_data(self, data: List[Tuple[str, float, float, float, float, int]]) -> int:
        """
        Insere os dados do IBovespa na tabela IBOV_Historico.

        :param data: Lista de tuplas (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        :return: Número de registros inseridos
        """
        if not data:
            return 0

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO dbo.IBOV_Historico (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.executemany(query, data)
        conn.commit()
        cursor.close()
        conn.close()

        return len(data)
    
    def get_ibov_data_by_date_range(self, start_date: str, end_date: str) -> List[Tuple[str, float, float, float, float, int]]:
        """
        Busca os dados do IBovespa dentro de um intervalo de datas.

        :param start_date: Data inicial (YYYY-MM-DD)
        :param end_date: Data final (YYYY-MM-DD)
        :return: Lista de tuplas (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT Data, Abertura, Alta, Baixa, Fechamento, Volume
        FROM dbo.IBOV_Historico
        WHERE Data BETWEEN ? AND ?
        ORDER BY Data ASC
        """

        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()

        return [(row.Data, row.Abertura, row.Alta, row.Baixa, row.Fechamento, row.Volume) for row in result]
    
    def insert_acao_data(self, data: List[Tuple]) -> int:
        """Insere múltiplos registros de ações na tabela"""
        if not data:
            return 0  # Não insere se não houver dados

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO dbo.Acao_Historico (Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(query, data)

        conn.commit()
        cursor.close()
        conn.close()

        return len(data)
    
    def get_acoes(self, codigo: str, start_date: str, end_date: str) -> List[Tuple]:
        """Consulta ações no banco de dados filtrando pelo código e intervalo de datas"""
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume
        FROM dbo.Acao_Historico
        WHERE Codigo = ? AND Data BETWEEN ? AND ?
        ORDER BY Data
        """
        cursor.execute(query, (codigo, start_date, end_date))
        result = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()

        return result