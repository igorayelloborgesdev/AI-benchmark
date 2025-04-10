from abc import ABC, abstractmethod
from typing import List

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