from abc import ABC, abstractmethod
from typing import List, Tuple

class IYFinanceAdapter(ABC):
    
    @abstractmethod
    def getRequest(self, ticker: str, start_date: str, end_date: str) -> List[Tuple]:
        """
        Busca os dados históricos de uma ação no Yahoo Finance.
        
        :param ticker: Código da ação (ex: "PETR4.SA")
        :param start_date: Data de início no formato YYYY-MM-DD
        :param end_date: Data de fim no formato YYYY-MM-DD
        :return: Lista de tuplas contendo (Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume)
        """
        pass    