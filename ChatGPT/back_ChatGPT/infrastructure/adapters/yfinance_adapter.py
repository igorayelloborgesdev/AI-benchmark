from typing import List, Tuple
from infrastructure.adapters.yfinance_adaptee import YFinanceAdaptee
from infrastructure.adapters.i_yfinance_adapter import IYFinanceAdapter

class YFinanceAdapter(IYFinanceAdapter):    
    def __init__(self, finance_adaptee: YFinanceAdaptee):
        self.finance_adaptee = finance_adaptee
    
    def getRequest(self, ticker: str, start_date: str, end_date: str) -> List[Tuple]:        
        return self.finance_adaptee.fetch_stock_data(ticker, start_date, end_date)
