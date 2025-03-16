from domain.repositories.i_finance_repository import IFinanceRepository
from domain.services.calculo_financeiro_service import CalculoFinanceiroService

class CalculoUseCase:
    def __init__(self, calculo_financeiro_service: CalculoFinanceiroService, repository: IFinanceRepository):
        self.repository = repository
        self.calculo_financeiro_service = calculo_financeiro_service

    def calcular_analise_risco(self, codigo: str, data_inicio: str, data_fim: str) -> float:
        
        historico_acao = self.repository.get_acoes(codigo, data_inicio, data_fim)
        historico_ibov = self.repository.get_ibov_data_by_date_range(data_inicio, data_fim)
        beta = self.calculo_financeiro_service.calcular_beta(historico_acao, historico_ibov)        
        cdi_data = self.repository.get_cdi_data(data_inicio, data_fim)
        if len(historico_acao) < 2 or not cdi_data:
            raise ValueError("Dados insuficientes para calcular o Sharpe Ratio.")
        sharpe = self.calculo_financeiro_service.calcular_sharpe_ratio(historico_acao, cdi_data)      
        fechamentos = [acao["Fechamento"] for acao in historico_acao]  
        volatilidade = self.calculo_financeiro_service.calcular_volatilidade(fechamentos)        
        retorno_esperado = self.calculo_financeiro_service.calcular_retorno_esperado(fechamentos)
        perda_estimada_valor_5 = self.calculo_financeiro_service.calcular_perda_estimada_valor(5.0, fechamentos)
        perda_estimada_percentual_5 = self.calculo_financeiro_service.calcular_perda_estimada_percentual(5.0, fechamentos)        
        is_super_estimada = self.calculo_financeiro_service.calcular_acao_superestimada_subestimada(historico_ibov, historico_acao, beta)
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

        
