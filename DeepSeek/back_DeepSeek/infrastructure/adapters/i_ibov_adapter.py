from abc import ABC, abstractmethod
from typing import List, Dict
from typing import Optional
from datetime import date

class IIBOVAdapter(ABC):
    @abstractmethod
    async def getRequest(self, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:        
        pass    