from abc import ABC, abstractmethod
from typing import List, Dict
from typing import Optional
from datetime import date

class IFinanceAdapter(ABC):
    @abstractmethod
    async def getRequest(self, codigo: str, data_inicial: date, data_final: date) -> List[Dict]:        
        pass    