from typing import List, Tuple
from infrastructure.adapters.yfinance_adapter import YFinanceAdapter
from infrastructure.repositories.finance_repository import IFinanceRepository

class YFinanceUseCase:
    """Caso de uso para buscar e armazenar dados de ações"""

    def __init__(self, adapter: YFinanceAdapter, finance_repository: IFinanceRepository):        
        self.adapter = adapter
        self.finance_repository = finance_repository

    def fetch_and_save_acao(self, codigo: str, start_date: str, end_date: str) -> int:
        """Busca os dados da ação no Yahoo Finance e salva no banco"""        
        data = self.adapter.getRequest(f"{codigo}.SA", start_date, end_date)                
        return self.finance_repository.insert_acao_data(data)        

    def get_acoes(self, codigo: str, start_date: str, end_date: str) -> List[Tuple]:
        """Consulta os dados da ação no banco"""        
        return self.finance_repository.get_acoes(codigo, start_date, end_date)