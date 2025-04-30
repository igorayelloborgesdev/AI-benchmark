from typing import List, Tuple
from datetime import date
import pandas as pd
import numpy as np

class FinancialService:
    def calculate_beta(
        self,        
        acao_historico,
        ibov_historico
    ):
        acao_retornos = [(acao['fechamento'] - acao_historico[i-1]['fechamento']) / acao_historico[i-1]['fechamento'] if i > 0 else 0 for i, acao in enumerate(acao_historico)]
        ibov_retornos = [(ibov['fechamento'] - ibov_historico[i-1]['fechamento']) / ibov_historico[i-1]['fechamento'] if i > 0 else 0 for i, ibov in enumerate(ibov_historico)]

        # Remova os valores iniciais de ambos os arrays até que eles tenham o mesmo tamanho
        min_len = min(len(acao_retornos), len(ibov_retornos))
        acao_retornos = acao_retornos[:min_len]
        ibov_retornos = ibov_retornos[:min_len]

        # Calcule a covariância e a variância
        covariancia = np.cov(acao_retornos, ibov_retornos)[0, 1]
        variancia = np.var(ibov_retornos)

        # Calcule o beta
        beta = covariancia / variancia

        return beta
    
    def calculate_sharpe(
        self,        
        acao_data: List[any],
        cdi_data: List[any]
    ):
        # Converter para dicionários por data
        acao_dict = {item['data']: item['fechamento'] for item in acao_data}
        cdi_dict = {item['data']: item['valor'] for item in cdi_data}
        
        # # Encontrar datas comuns
        # common_dates = sorted(set(acao_dict.keys()) & set(cdi_dict.keys()))
        
        # if len(common_dates) < 2:
        #     raise ValueError("Dados insuficientes para cálculo (mínimo 2 dias)")
        
        # Calcular retornos diários da ação e do CDI
        acao_prices = list(acao_dict.values())
        cdi_rates = list(cdi_dict.values())
        
        # Converter taxas CDI de porcentagem anual para diária (252 dias úteis)
        cdi_daily = [(1 + rate/100)**(1/252) - 1 for rate in cdi_rates[:-1]]
        
        # Calcular retornos logarítmicos diários da ação
        acao_returns = np.diff(np.log(acao_prices))
        
        min_len = min(len(acao_returns), len(cdi_daily))
        acao_returns = acao_returns[:min_len]
        cdi_daily = cdi_daily[:min_len]

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