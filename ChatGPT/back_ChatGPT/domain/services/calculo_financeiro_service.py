import numpy as np
from datetime import date, timedelta
from typing import List, Tuple

class CalculoFinanceiroService:
    def calcular_beta(self, historico_acao: List[Tuple], historico_ibov: List[Tuple[str, float, float, float, float, int]]):
        if not historico_acao or not historico_ibov:
            raise ValueError("Dados insuficientes para calcular o Beta.")

        # Criar dicionário para rápida busca dos preços de fechamento
        ibov_dict = {item["Data"]: item["Fechamento"] for item in historico_ibov}

        # Filtrar apenas datas que existem nos dois conjuntos
        retornos_acao, retornos_ibov = [], []

        for item in historico_acao:
            if item["Data"] in ibov_dict:
                fechamento_ibov_anterior = ibov_dict.get(item["Data"] - timedelta(days=1))
                fechamento_acao_anterior = next((x["Fechamento"] for x in historico_acao if x["Data"] == item["Data"] - timedelta(days=1)), None)
                
                if fechamento_ibov_anterior and fechamento_acao_anterior:
                    retorno_acao = (item["Fechamento"] - fechamento_acao_anterior) / fechamento_acao_anterior
                    retorno_ibov = (ibov_dict[item["Data"]] - fechamento_ibov_anterior) / fechamento_ibov_anterior

                    retornos_acao.append(retorno_acao)
                    retornos_ibov.append(retorno_ibov)

        if len(retornos_acao) < 2:
            raise ValueError("Dados insuficientes para calcular o Beta.")

        # # Regressão linear para calcular Beta
        retornos_acao = np.array(retornos_acao)
        retornos_ibov = np.array(retornos_ibov)

        cov_matrix = np.cov(retornos_acao, retornos_ibov)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1]
        return beta