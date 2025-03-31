from abc import ABC, abstractmethod
from typing import List, Dict
from typing import Optional
from datetime import date

class IFinanceAdapter(ABC):
    @abstractmethod
    async def getRequest(self, codigo: str, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:        
        pass    