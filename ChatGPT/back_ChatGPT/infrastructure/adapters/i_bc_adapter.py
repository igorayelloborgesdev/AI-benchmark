from abc import ABC, abstractmethod
from typing import List, Dict

class IBCAdapter(ABC):
    """Interface para o caso de uso de processamento de Excel."""

    @abstractmethod
    async def getRequest(self) -> List[Dict]:        
        pass    