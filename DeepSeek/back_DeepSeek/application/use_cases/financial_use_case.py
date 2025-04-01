from infrastructure.adapters.cdi_adapter import CDIAdapter
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.yfinance_adapter import IFinanceAdapter
from domain.repositories.i_financial_repository import IFinancialRepository
from typing import Optional, Tuple
from datetime import date
from domain.services.financial_service import FinancialService

class FinancialUseCase:
    def __init__ (self, cdi_adapter: CDIAdapter, ibov_adapter: IBOVAdapter, finance_adapter: IFinanceAdapter, financial_repository: IFinancialRepository):
        self.cdi_adapter = cdi_adapter
        self.financial_repository = financial_repository
        self.ibov_adapter = ibov_adapter
        self.finance_adapter = finance_adapter

    def financial_service_builder(self, financial_service: FinancialService):
        self.financial_service = financial_service

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

    def calculate_financial_analisis(self, codigo: str, start_date: date, end_date: date):
        # Obter dados históricos
        ibov_data = self.get_historical_data(start_date, end_date)
        acao_data = self.get_historical_data_stock(codigo, start_date, end_date)
        beta = self.financial_service.calculate_beta(codigo, acao_data, ibov_data, start_date, end_date)
        cdi_data = self.execute_get_cdis_by_date_range(start_date, end_date)        
        sharpe = self.financial_service.calculate_sharpe(codigo, acao_data, cdi_data, start_date, end_date)
        fechamentos = [acao["fechamento"] for acao in acao_data]          
        volatilidade = self.financial_service.calcular_volatilidade(fechamentos)        
        retorno_esperado = self.financial_service.calcular_retorno_esperado(fechamentos)        
        perda_estimada_valor_5 = self.financial_service.calcular_perda_estimada_valor(5.0, fechamentos)        
        perda_estimada_percentual_5 = self.financial_service.calcular_perda_estimada_percentual(5.0, fechamentos)                
        is_super_estimada = self.financial_service.calcular_acao_superestimada_subestimada(ibov_data, acao_data, beta)        
        return {
            "Codigo": codigo,
            "Beta": beta,
            "Sharpe": sharpe,
            "Volatilidade": volatilidade,
            "Retorno esperado": retorno_esperado,
            "Perda estimada valor 5%": perda_estimada_valor_5,
            "Perda estimada percentual 5%": perda_estimada_percentual_5,
            "Super estimada": is_super_estimada
        }