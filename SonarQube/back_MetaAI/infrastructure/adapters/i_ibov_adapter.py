from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import date

class IIBOVAdapter(ABC):
    @abstractmethod
    async def getRequest(self, data_inicial: date, data_final: date) -> List[Dict]:        
        pass    