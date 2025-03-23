from abc import ABC, abstractmethod

class IRepositorioSegmento(ABC):
    @abstractmethod
    def salvar_segmento_classificacao(self, segmentos: list):
        """
        Salva uma lista de segmentos no banco de dados.
        """
        pass

    @abstractmethod
    def salvar_setor_economico(self, records):
        """
        Insere os registros no banco de dados SQL Server.
        """
        pass

    @abstractmethod
    def salvar_sub_setor_economico(self, records):
        """
        Insere os registros no banco de dados SQL Server.
        """
        pass

    @abstractmethod
    def salvar_segmento(self, records):
        """
        Insere os registros filtrados no banco de dados SQL Server.
        """
        pass

    @abstractmethod
    def obter_id(self, tabela, coluna, valor):
        """
        Busca o ID em uma tabela pelo valor em uma coluna.
        """
        pass

    @abstractmethod
    def salvar_empresa(self, records):
        """
        Insere os registros na tabela dbo.Empresa.
        """
        pass

    @abstractmethod
    def get_all_segmento_classificacao(self):
        pass

    @abstractmethod
    def get_segmentos(self):
        pass

    @abstractmethod
    def get_setor_economico(self):
        pass

    @abstractmethod
    def get_sub_setor(self):
        pass

    @abstractmethod
    def get_empresa_by_codigo(self, codigo: str):
        pass
