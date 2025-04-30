from infrastructure.adapters.cdi_adapter import CDIAdapter
from domain.repositories.i_bovespa_repository import IBovespaRepository
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.yfinance_adapter import FinanceAdapter
from domain.services.financial_service import FinancialService

class FinancialUseCase:
    def __init__ (self, bovespa_repository: IBovespaRepository):        
        self.bovespa_repository = bovespa_repository
    def cdi_builder(self, cdi_adapter: CDIAdapter):
        self.cdi_adapter = cdi_adapter
        return self
    def ibov_builder(self, ibov_adapter: IBOVAdapter):
        self.ibov_adapter = ibov_adapter
        return self
    def finance_builder(self, finance_adapter: FinanceAdapter):
        self.finance_adapter = finance_adapter
        return self    
    def financial_service_builder(self, financial_service: FinancialService):
        self.financial_service = financial_service
        return self

    def post_cdi_data(self, data_inicial: str, data_final: str):
        cdi_data = self.cdi_adapter.getRequest(data_inicial, data_final)
        self.bovespa_repository.save_cdi_data(cdi_data)

    def get_cdi_data(self, data_inicial: str, data_final: str):
        return self.bovespa_repository.get_cdi_data(data_inicial, data_final)
    
    async def post_ibov_data(self, start_date: str, end_date: str):
        ibov_data = await self.ibov_adapter.getRequest(start_date, end_date)
        return self.bovespa_repository.save_ibov_data(ibov_data)        
    
    def get_ibov_data(self, data_inicial: str, data_final: str):
        return self.bovespa_repository.get_ibov_data(data_inicial, data_final)
    
    async def post_acao_data(self, codigo: str, start_date: str, end_date: str):
        acoes = await self.finance_adapter.getRequest(codigo, start_date, end_date)
        return self.bovespa_repository.save_acoes_data(acoes, codigo)    
    
    def get_acao_data(self, codigo: str, start_date: str, end_date: str):
        return self.bovespa_repository.get_acao_data(codigo, start_date, end_date)
    
    def calculate_acao_sharpe_ratio(self, codigo: str, start_date: str, end_date: str):
        ibov_data = self.bovespa_repository.get_ibov_data(start_date, end_date)
        acao_data = self.bovespa_repository.get_acao_data(codigo, start_date, end_date)        
        beta = self.financial_service.calculate_beta(ibov_data, acao_data)
        cdi_data = self.bovespa_repository.get_cdi_data(start_date, end_date)        
        sharpe = self.financial_service.calculate_sharpe(acao_data, cdi_data)
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
