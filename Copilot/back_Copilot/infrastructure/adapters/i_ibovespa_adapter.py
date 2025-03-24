from abc import ABC, abstractmethod
from typing import List, Dict

class IIBovespaAdapter(ABC):
    
    @abstractmethod
    def getRequest(self, start_date: str, end_date: str) -> List[Dict]:
        pass    