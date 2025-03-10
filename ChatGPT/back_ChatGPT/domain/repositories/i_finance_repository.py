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