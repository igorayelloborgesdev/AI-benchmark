import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

class FinancialService:
    def calcular_beta(self, ibov_data_list: List[Dict], acao_data_list: List[Dict]):
        acao_data = pd.DataFrame(acao_data_list)
        ibov_data = pd.DataFrame(ibov_data_list)

        # Garantir que as datas coincidem entre os datasets
        merged_data = acao_data.merge(ibov_data, on="Data", suffixes=("_acao", "_ibov"))

        # Calcular os retornos diários
        merged_data["retorno_acao"] = merged_data["Fechamento_acao"].pct_change()
        merged_data["retorno_ibov"] = merged_data["Fechamento_ibov"].pct_change()

        # Remover valores NaN gerados pelo cálculo de retornos
        merged_data = merged_data.dropna()

        # Calcular covariância e variância
        cov = np.cov(merged_data["retorno_acao"], merged_data["retorno_ibov"])[0, 1]
        var = np.var(merged_data["retorno_ibov"])

        # Retornar Beta
        return cov / var
    
    def calcular_sharpe_ratio(self, historico_acao: List[Dict], cdi_data: List[Dict]):
        """
        Calcula o índice de Sharpe de uma ação.
        :param rf: Retorno livre de risco (ex: CDI médio no período)
        :return: Índice de Sharpe
        """        
        if len(historico_acao) < 2 or not cdi_data:
            raise ValueError("Dados insuficientes para calcular o Sharpe Ratio.")        
        # Ordenar os dados por data
        historico_acao.sort(key=lambda x: x["Data"])        
        # Extrair preços de fechamento
        precos = [item["Fechamento"] for item in historico_acao]        
        # Calcular os retornos diários da ação
        retornos_acao = [((precos[i] / precos[i - 1]) - 1) * 100.0 for i in range(1, len(precos))]        
        cdi_tuples = [(item["Data"], item["Valor"]) for item in cdi_data]
        # Calcular a média do CDI diário no período
        cdi_medio = np.mean([cdi[1] for cdi in cdi_tuples])                
        # Cálculo do Sharpe Ratio
        retorno_medio = np.mean(retornos_acao)
        volatilidade = np.std(retornos_acao, ddof=1)  # Desvio padrão amostral        
        if volatilidade == 0:
            return float("nan")  # Evita divisão por zero        
        sharpe_ratio = (retorno_medio - cdi_medio) / volatilidade
        return sharpe_ratio
    
    def calcular_volatilidade(self, fechamentos: List[float]) -> float:
        if len(fechamentos) < 2:
            raise ValueError("Dados insuficientes para calcular a volatilidade.")        
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0  # Calcula os retornos percentuais                
        volatilidade = np.std(retornos_diarios) # Ajuste anualizado        
        return round(volatilidade, 6)  # Arredonda para melhor legibilidade
    
    def calcular_retorno_esperado(self, fechamentos: List[float]) -> float:    
        """
        Calcula o retorno esperado de uma ação em um intervalo de datas.
        """        
        # Calcular os retornos diários
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0
        # Calcular o retorno esperado (média dos retornos)
        retorno_esperado = np.mean(retornos_diarios)
        return round(retorno_esperado, 4)  # Arredonda o valor para 4 casas decimais
    
    def calcular_perda_estimada_valor(self, perc: float, fechamentos: List[float]) -> float:    
        percentil = np.percentile(fechamentos, perc)
        return percentil
    
    def calcular_perda_estimada_percentual(self, perc: float, fechamentos: List[float]) -> float:    
        retornos_diarios = (np.diff(fechamentos) / fechamentos[:-1]) * 100.0
        percentil = np.percentile(retornos_diarios, perc)
        return percentil
    
    def calcular_acao_superestimada_subestimada(self, registros_ibov: List[Tuple[str, float, float, float, float, int]], registros_acao: List[Tuple], beta: float) -> bool:    
        ibov_ultimos_dois = registros_ibov[-2:] if len(registros_ibov) >= 2 else registros_ibov
        ibov_diff = ((ibov_ultimos_dois[1]['Fechamento'] * 100.0)/ibov_ultimos_dois[0]['Fechamento']) - 100.0
        acoes_ultimos_dois = registros_acao[-2:] if len(registros_acao) >= 2 else registros_acao
        acoes_diff = ((acoes_ultimos_dois[1]['Fechamento'] * 100.0)/acoes_ultimos_dois[0]['Fechamento']) - 100.0
        ret_exp = ibov_diff * beta
        is_super_estimada = True if ret_exp >= acoes_diff else False        
        return is_super_estimada
        