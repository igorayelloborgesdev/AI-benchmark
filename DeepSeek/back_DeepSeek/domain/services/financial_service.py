from typing import List, Tuple
import numpy as np
from datetime import date

class FinancialService:
    def calculate_beta(
        self,
        codigo: str,
        acao_data: List[any],
        ibov_data: List[any],
        start_date: date,
        end_date: date
    ):
        # Alinhar os dados por data
        # Converter listas de dicionários para dicionários indexados por data
        acao_dict = {item['data']: item['fechamento'] for item in acao_data}
        ibov_dict = {date.fromisoformat(item['data']) if isinstance(item['data'], str) else item['data']: item['fechamento'] for item in ibov_data}
        
        # Pegar apenas datas presentes em ambos
        common_dates = sorted(set(acao_dict.keys()) & set(ibov_dict.keys()))
        if len(common_dates) < 2:
            raise ValueError("Dados insuficientes para cálculo do Beta (mínimo 2 dias)")
        
        # Preparar arrays de retornos
        acao_prices = [acao_dict[date] for date in common_dates]
        ibov_prices = [ibov_dict[date] for date in common_dates]
        
        # Calcular retornos percentuais diários
        acao_returns = np.diff(acao_prices) / acao_prices[:-1]
        ibov_returns = np.diff(ibov_prices) / ibov_prices[:-1]
        
        # Calcular covariância e variância
        covariance = np.cov(acao_returns, ibov_returns)[0][1]
        variance = np.var(ibov_returns)
        
        beta = covariance / variance

        return beta
     
    def calculate_sharpe(
        self,
        codigo: str,
        acao_data: List[any],
        cdi_data: List[any],
        start_date: date,
        end_date: date
    ):
        # Converter para dicionários por data
        acao_dict = {item['data']: item['fechamento'] for item in acao_data}
        cdi_dict = {item['data']: item['valor'] for item in cdi_data}
        
        # Encontrar datas comuns
        common_dates = sorted(set(acao_dict.keys()) & set(cdi_dict.keys()))
        
        if len(common_dates) < 2:
            raise ValueError("Dados insuficientes para cálculo (mínimo 2 dias)")
        
        # Calcular retornos diários da ação e do CDI
        acao_prices = [acao_dict[d] for d in common_dates]
        cdi_rates = [cdi_dict[d] for d in common_dates]
        
        # Converter taxas CDI de porcentagem anual para diária (252 dias úteis)
        cdi_daily = [(1 + rate/100)**(1/252) - 1 for rate in cdi_rates[:-1]]
        
        # Calcular retornos logarítmicos diários da ação
        acao_returns = np.diff(np.log(acao_prices))
        
        # Calcular componentes do Sharpe
        excess_returns = acao_returns - cdi_daily
        avg_excess_return = np.mean(excess_returns) * 252  # Anualizado
        volatility = np.std(acao_returns) * np.sqrt(252)  # Anualizado
        
        if volatility == 0:
            raise ValueError("Volatilidade zero - impossível calcular Sharpe")
        
        sharpe_ratio = avg_excess_return / volatility
        return sharpe_ratio

    def calcular_volatilidade(self, fechamentos: List[float]):
        if len(fechamentos) < 2:
            raise ValueError("Dados insuficientes para calcular a volatilidade.")        
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0  # Calcula os retornos percentuais                
        volatilidade = np.std(retornos_diarios) # Ajuste anualizado        
        return round(volatilidade, 6)  # Arredonda para melhor legibilidade
    
    def calcular_retorno_esperado(self, fechamentos: List[float]):            
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0        
        retorno_esperado = np.mean(retornos_diarios)
        return round(retorno_esperado, 4)  # Arredonda o valor para 4 casas decimais
    
    def calcular_perda_estimada_valor(self, perc: float, fechamentos: List[float]):    
        percentil = np.percentile(fechamentos, perc)
        return percentil
    
    def calcular_perda_estimada_percentual(self, perc: float, fechamentos: List[float]):    
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0
        percentil = np.percentile(retornos_diarios, perc)
        return percentil
    
    def calcular_acao_superestimada_subestimada(self, registros_ibov: List[Tuple[str, float, float, float, float, int]], registros_acao: List[Tuple], beta: float):    
        ibov_ultimos_dois = registros_ibov[-2:] if len(registros_ibov) >= 2 else registros_ibov
        ibov_diff = ((ibov_ultimos_dois[1]['fechamento'] * 100.0)/ibov_ultimos_dois[0]['fechamento']) - 100.0
        acoes_ultimos_dois = registros_acao[-2:] if len(registros_acao) >= 2 else registros_acao
        acoes_diff = ((acoes_ultimos_dois[1]['fechamento'] * 100.0)/acoes_ultimos_dois[0]['fechamento']) - 100.0
        ret_exp = ibov_diff * beta
        is_super_estimada = True if ret_exp >= acoes_diff else False        
        return is_super_estimada