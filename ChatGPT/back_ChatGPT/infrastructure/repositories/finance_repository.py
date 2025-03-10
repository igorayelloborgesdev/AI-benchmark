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