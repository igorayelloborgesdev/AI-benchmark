import numpy as np
import pandas as pd
from typing import List, Dict

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