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
    
    def calcular_sharpe_ratio(self, historico_acao: List[Tuple], cdi_data: List[Tuple[str, float]]):
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

        # Calcular a média do CDI diário no período
        cdi_medio = np.mean([cdi[1] for cdi in cdi_data])        

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
        