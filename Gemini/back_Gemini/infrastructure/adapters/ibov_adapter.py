from typing import List, Dict
from infrastructure.adapters.ibov_adaptee import IBOVAdaptee
from infrastructure.adapters.i_ibov_adapter import IIBOVAdapter
from datetime import date

class IBOVAdapter(IIBOVAdapter):    
    def __init__(self, ibov_adaptee: IBOVAdaptee):
        self.ibov_adaptee = ibov_adaptee
    
    async def getRequest(self, data_inicial: date, data_final: date) -> List[Dict]:                        
        return await self.ibov_adaptee.fetch_historical_data(data_inicial, data_final)
