from infrastructure.adapters.cdi_adapter import CDIAdapter
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.yfinance_adapter import FinanceAdapter
from domain.repositories.i_bovespa_repository import IBovespaRepository
from datetime import date

class FinancialUseCase:
    def __init__ (self, cdi_adapter: CDIAdapter, ibov_adapter: IBOVAdapter, finance_adapter: FinanceAdapter, bovespa_repository: IBovespaRepository):
        self.cdi_adapter = cdi_adapter
        self.ibov_adapter = ibov_adapter
        self.bovespa_repository = bovespa_repository
        self.finance_adapter = finance_adapter
        
    async def fetch_and_save_cdi(self, data_inicial: str, data_final: str):
        try:
            cdi_lista = await self.cdi_adapter.getRequest(data_inicial, data_final)                      
            await self.bovespa_repository.save_cdi_data(cdi_lista)            
            return {
                "message": f"Dados do CDI atualizados com sucesso"                
            }
        except Exception as e:
            return {
                "error": str(e),
                "registros_inseridos": 0
            }        
        
    async def fetch_and_save_ibov(self, start_date: date, end_date: date):
        try:
            ibov = await self.ibov_adapter.getRequest(start_date, end_date)                      
            await self.bovespa_repository.save_ibov_data(ibov)
            return {
                "message": f"Dados do Ibovespa atualizados com sucesso"                
            }
        except Exception as e:
            return {
                "error": str(e),
                "registros_inseridos": 0
            }        
        

    async def get_ibov_by_date_range(self, codigo: str, start_date: date, end_date: date):
        try:
            stock = await self.finance_adapter.getRequest(codigo, start_date, end_date)                      
            await self.bovespa_repository.save_stock_data(stock)
            return {
                "message": f"Dados do Ibovespa atualizados com sucesso"                
            }
        except Exception as e:
            return {
                "error": str(e),
                "registros_inseridos": 0
            }        