from abc import ABC, abstractmethod
from typing import List

class IBovespaRepository(ABC):
    @abstractmethod
    def create_segmentos_economicos(self, sigla, descritivo):
        pass
