from abc import ABC, abstractmethod
from typing import List, Tuple

class IIBovespaAdapter(ABC):
    
    @abstractmethod
    async def getRequest(self, start_date: str, end_date: str) -> List[Tuple[str, float, float, float, float, int]]:
        pass    