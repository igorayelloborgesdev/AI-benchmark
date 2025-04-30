from abc import ABC, abstractmethod

class IBovespaRepository(ABC):

    @abstractmethod
    def create_segmentos_economicos(self, segmentos):
        pass

    @abstractmethod
    def get_segmentos_classificacao(self):
        pass

    @abstractmethod
    def create_setores_economicos(self, setores_economicos):
        pass

    @abstractmethod
    def get_setores_economicos(self):
        pass

    @abstractmethod
    def create_sub_setores(self, sub_setores):
        pass

    @abstractmethod
    def get_sub_setores(self):
        pass

    @abstractmethod
    def create_segmentos(self, segmentos):
        pass

    @abstractmethod
    def get_segmentos(self):
        pass

    @abstractmethod
    def buscar_segmento_classificacao_id(self, sigla):
        pass
    
    @abstractmethod
    def buscar_setor_economico_id(self, descritivo):
        pass

    # Função para buscar o ID da tabela Subsetor
    def buscar_subsetor_id(self, descritivo):
        pass

    # Função para buscar o ID da tabela Segmento
    def buscar_segmento_id(self, descritivo):
        pass

    @abstractmethod
    def create_empresas(self, empresas):
        pass

    @abstractmethod
    def get_empresa_by_codigo(self, codigo):
        pass

    @abstractmethod
    def save_cdi_data(self, cdi_data):
        pass

    @abstractmethod
    def get_cdi_data(self, data_inicial, data_final):
        pass

    @abstractmethod
    def save_ibov_data(self, data):
        pass

    @abstractmethod
    def get_ibov_data(self, data_inicial: str, data_final: str):
        pass

    @abstractmethod
    def save_acoes_data(self, data, codigo):
        pass

    @abstractmethod
    def get_acao_data(self, codigo: str, start_date: str, end_date: str):
        pass