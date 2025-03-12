from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class IFinanceRepository(ABC):

    abstractmethod
    def insert_cdi_data(self, data: List[Tuple[str, float]]) -> int:
        """Insere múltiplos registros na tabela CDI_Diario."""
        pass
    
    @abstractmethod
    def get_cdi_data(self, data_inicial: Optional[str], data_final: Optional[str]) -> List[Tuple[str, float]]:
        """
        Busca os dados do CDI filtrando por data inicial e final.

        :param data_inicial: Data inicial no formato 'yyyy-MM-dd' (opcional).
        :param data_final: Data final no formato 'yyyy-MM-dd' (opcional).
        :return: Lista de tuplas [(Data, Valor)].
        """
        pass

    @abstractmethod
    def insert_ibov_data(self, data: List[Tuple[str, float, float, float, float, int]]) -> int:
        """
        Insere os dados do IBovespa na tabela IBOV_Historico.

        :param data: Lista de tuplas (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        :return: Número de registros inseridos
        """
        pass

    @abstractmethod
    def get_ibov_data_by_date_range(self, start_date: str, end_date: str) -> List[Tuple[str, float, float, float, float, int]]:
        """
        Busca os dados do IBovespa dentro de um intervalo de datas.

        :param start_date: Data inicial (YYYY-MM-DD)
        :param end_date: Data final (YYYY-MM-DD)
        :return: Lista de tuplas (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        """
        pass