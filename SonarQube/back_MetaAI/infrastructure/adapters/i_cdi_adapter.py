from abc import ABC, abstractmethod
from typing import List, Dict

class ICDIAdapter(ABC):
    @abstractmethod
    def getRequest(self, data_inicial: str, data_final: str) -> List[Dict]:        
        pass    