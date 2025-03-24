from typing import List, Tuple
from infrastructure.adapters.ibovespa_adaptee import IBovespaAdaptee
from infrastructure.adapters.i_ibovespa_adapter import IIBovespaAdapter

class IBovespaAdapter(IIBovespaAdapter):    
    def __init__(self, bovespa_adaptee: IBovespaAdaptee):
        self.bovespa_adaptee = bovespa_adaptee
    
    def getRequest(self, start_date: str, end_date: str) -> List[Tuple[str, float, float, float, float, int]]:
        return self.bovespa_adaptee.get_historical_data(start_date, end_date)
