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
        return beta

        
