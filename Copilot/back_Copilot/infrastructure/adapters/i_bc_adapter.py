from abc import ABC, abstractmethod
from typing import List, Dict

class IBCAdapter(ABC):    
    @abstractmethod
    async def getRequest(self) -> List[Dict]:        
        pass    