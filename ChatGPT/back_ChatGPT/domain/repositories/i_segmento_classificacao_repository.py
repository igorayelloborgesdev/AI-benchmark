from abc import ABC, abstractmethod
from typing import List, Tuple

class ISegmentoClassificacaoRepository(ABC):
    """Interface para operações no banco de dados SegmentoClassificacao."""

    @abstractmethod
    def insert_many(self, data: List[Tuple[str, str]]) -> int:
        """Insere múltiplos registros no banco de dados e retorna a quantidade inserida."""
        pass

    @abstractmethod
    def insert_many_setor_economico(self, data: List[str]) -> int:        
        pass

    @abstractmethod
    def insert_many_subsetor(self, data: List[str]) -> int:        
        pass

    @abstractmethod
    def insert_many_segmento_economico(self, data: List[str]) -> int:        
        pass
