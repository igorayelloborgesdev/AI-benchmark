from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

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
    
    @abstractmethod
    async def get_segmento_classificacao_id(self, sigla: Optional[str]) -> Optional[int]:
        pass

    @abstractmethod
    async def get_setor_economico_id(self, descritivo: Optional[str]) -> Optional[int]:
        pass

    @abstractmethod
    async def get_subsetor_id(self, descritivo: Optional[str]) -> Optional[int]:
        pass

    @abstractmethod
    async def get_segmento_id(self, descritivo: Optional[str]) -> Optional[int]:
        pass

    @abstractmethod
    async def insert_many_empresas(self, empresas: List[Tuple[str, str, Optional[int], int, int, int]]) -> int:
        pass

    @abstractmethod
    def get_all_segmento_classificacao(self) -> List[Tuple[int, str, str]]:
        pass

    @abstractmethod
    def get_all_setor_economico(self) -> List[Tuple[int, str]]:
        pass

    @abstractmethod
    def get_all_subsetor(self) -> List[Tuple[int, str]]:
        pass

    @abstractmethod
    def get_all_segmento(self) -> List[Tuple[int, str]]:
        pass

    @abstractmethod
    def get_empresa_by_codigo(self, codigo: Optional[str] = None) -> List[Tuple[int, str, str, str, str, str, str]]:
        pass