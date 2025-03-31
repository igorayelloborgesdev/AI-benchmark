from infrastructure.adapters.cdi_adapter import CDIAdapter
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.yfinance_adapter import IFinanceAdapter
from domain.repositories.i_financial_repository import IFinancialRepository
from typing import Optional, Tuple
from datetime import date

class FinancialUseCase:
    def __init__ (self, cdi_adapter: CDIAdapter, ibov_adapter: IBOVAdapter, finance_adapter: IFinanceAdapter, financial_repository: IFinancialRepository):
        self.cdi_adapter = cdi_adapter
        self.financial_repository = financial_repository
        self.ibov_adapter = ibov_adapter
        self.finance_adapter = finance_adapter

    async def execute_fetch_and_store(self,  data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> dict:
        try:
            cdi_lista = await self.cdi_adapter.getRequest(data_inicial, data_final)          
            count = self.financial_repository.create_cdis(cdi_lista)                        
            return {
                "message": f"Dados do CDI atualizados com sucesso",
                "registros_inseridos": count                
            }
        except Exception as e:
            return {
                "error": str(e),
                "registros_inseridos": 0
            }
        
    def execute_get_cdis_by_date_range(
        self,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None
    ):
        return self.financial_repository.get_cdis_by_date_range(data_inicial, data_final)
    
    async def fetch_ibov_data(self, start_date: date, end_date: date) -> Tuple[int, int]:        
        data = await self.ibov_adapter.getRequest(start_date, end_date)
        saved_count = self.financial_repository.save_historical_data(data)                
        return (len(data), saved_count)
    
    def get_historical_data(self, start_date=None, end_date=None):
        return self.financial_repository.get_historical_data(start_date, end_date)                
    
    async def fetch_acao_data(self, codigo: str, start_date: date, end_date: date) -> Tuple[int, int]:
        data = await self.finance_adapter.getRequest(codigo, start_date, end_date)        
        saved_count = self.financial_repository.save_historical_data(data)                
        return (len(data), saved_count)        
    
    def get_historical_data_stock(self,
        codigo: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None):
        return self.financial_repository.get_historical_data_stock(codigo, start_date, end_date)                

