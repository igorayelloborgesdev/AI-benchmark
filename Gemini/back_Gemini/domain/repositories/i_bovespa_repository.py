from abc import ABC, abstractmethod
from typing import List
from datetime import date

class IBovespaRepository(ABC):
    @abstractmethod
    def create_segmentos_economicos(self, sigla, descritivo):
        pass

    @abstractmethod
    def get_all_segmentos_classifcacao(self):
        pass

    @abstractmethod
    def create_subsetor(self, subsetores_a_inserir):
        pass

    @abstractmethod
    def get_all_subsetores(self):
        pass

    @abstractmethod
    def create_subsetores(self, setores_a_inserir):
        pass

    @abstractmethod
    def get_all_setores(self):
        pass

    @abstractmethod
    def create_segmentos(self, segmentos_a_inserir):
        pass 

    @abstractmethod
    def get_all_segmentos(self):
        pass 

    @abstractmethod
    async def get_segmento_classificacao_id(self, sigla: str):
        pass 

    @abstractmethod
    async def get_setor_economico_id(self, descritivo: str):
        pass 

    @abstractmethod    
    async def get_subsetor_id(self, descritivo: str):
        pass 
        
    @abstractmethod
    async def get_segmento_id(self, descritivo: str):
        pass 

    @abstractmethod
    async def inserir_empresas(self, empresas_a_inserir):
        pass 

    @abstractmethod
    async def get_empresa_by_id(self, empresa_id: str):
        pass 

    @abstractmethod
    async def save_cdi_data(self, data: List):
        pass 

    @abstractmethod
    async def get_cdi_by_date_range(self, data_inicial: date, data_final: date):
        pass 

    @abstractmethod
    async def save_ibov_data(self, data: List):
        pass 

    @abstractmethod
    async def get_ibov_by_date_range(self, data_inicial: date, data_final: date):
        pass 

    @abstractmethod
    async def save_stock_data(self, data: List):
        pass 

    @abstractmethod
    def get_acao_historico(self, codigo: str, data_inicial: date, data_final: date) -> List:
        pass 