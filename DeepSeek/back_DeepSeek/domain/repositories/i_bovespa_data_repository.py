from abc import ABC, abstractmethod
from typing import List

class ISegmentoRepository(ABC):
    @abstractmethod
    def create_segmentos_economicos(self, segmentos: List[any]):
        pass
    
    @abstractmethod
    def get_segmentos_economicos(self):
        pass

    @abstractmethod
    def create_sub_setor(self, sub_setores: List[any]):
        pass

    @abstractmethod
    def get_subsetores(self):
        pass

    @abstractmethod
    def create_setor_economico(self, setor_economico: List[any]):
        pass

    @abstractmethod
    def get_setores(self):
        pass

    @abstractmethod
    def create_segmentos(self, segmentos: List[any]):
        pass

    @abstractmethod
    def get_segmentos(self):
        pass

    @abstractmethod
    def get_segmento_classificacao_id_by_sigla(self, sigla: str):
        pass

    @abstractmethod
    def get_setor_economico_id_by_descritivo(self, descritivo: str):
        pass

    @abstractmethod
    def get_subsetor_id_by_descritivo(self, descritivo: str):
        pass

    @abstractmethod
    def get_segmento_id_by_descritivo(self, descritivo: str):
        pass

    @abstractmethod
    def create_empresas(self, empresas: List[any]):
        pass

    @abstractmethod
    def get_empresa_by_codigo(self, codigo: str):
        pass