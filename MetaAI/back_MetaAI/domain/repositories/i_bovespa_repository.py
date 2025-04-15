from abc import ABC, abstractmethod

class IBovespaRepository(ABC):

    @abstractmethod
    def create_segmentos_economicos(self, segmentos):
        pass

    @abstractmethod
    def get_segmentos_classificacao(self):
        pass