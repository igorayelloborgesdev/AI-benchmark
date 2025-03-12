from datetime import datetime, timedelta
from infrastructure.adapters.ibovespa_adapter import IBovespaAdapter
from infrastructure.repositories.finance_repository import IFinanceRepository

class IBovespaUseCase:
    """Caso de uso para buscar e armazenar dados do IBovespa."""
    
    def __init__(self, adapter: IBovespaAdapter, finance_repository: IFinanceRepository):
        self.adapter = adapter
        self.finance_repository = finance_repository

    async def fetch_and_store_ibov_data(self, start_date: str, end_date: str) -> int:
        """
        Consulta os dados do IBovespa e armazena no banco de dados.

        :param start_date: Data inicial (YYYY-MM-DD)
        :param end_date: Data final (YYYY-MM-DD)
        :return: Número de registros inseridos
        """        
        data = await self.adapter.getRequest(start_date, end_date)        
        return self.finance_repository.insert_ibov_data(data)
    
    def get_ibov_data(self, start_date: str, end_date: str):
        """
        Consulta os dados do IBovespa dentro de um intervalo de datas.

        :param start_date: Data inicial (YYYY-MM-DD)
        :param end_date: Data final (YYYY-MM-DD)
        :return: Lista de dados históricos do IBovespa
        """
        return self.finance_repository.get_ibov_data_by_date_range(start_date, end_date)
