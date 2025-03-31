from typing import List, Dict
from infrastructure.adapters.yfinance_adaptee import FinanceAdaptee
from infrastructure.adapters.i_yfinance_adapter import IFinanceAdapter
from typing import Optional
from datetime import date

class FinanceAdapter(IFinanceAdapter):    
    def __init__(self, finance_adaptee: FinanceAdaptee):
        self.finance_adaptee = finance_adaptee
    
    async def getRequest(self, codigo: str, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:        
        return await self.finance_adaptee.fetch_acao_data(codigo, data_inicial, data_final)
