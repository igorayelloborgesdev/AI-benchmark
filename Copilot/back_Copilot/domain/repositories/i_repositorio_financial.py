from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class IRepositorioFinancial(ABC):
    @abstractmethod
    def salvar_cdi_diario(self, dados: List[Dict]):
        """
        Salva uma lista de segmentos no banco de dados.
        """
        pass

    @abstractmethod
    def get_cdi_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os registros da tabela CDI_Diario filtrados pelo intervalo de datas.
        
        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        """
        pass

    @abstractmethod
    def salvar_dados(self, dados: List[Dict]):
        """
        Insere os dados na tabela IBovespa_Dados.
        """
        pass

    @abstractmethod
    def get_ibov_historico_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os registros do IBOV_Historico filtrados pelo intervalo de datas.

        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        """
        pass

    @abstractmethod
    def salvar_dados_acoes(self, dados: List[Dict]):
        """
        Insere os dados das ações na tabela Acoes_Bovespa.
        """
        pass

    @abstractmethod
    def get_historico_por_acao_e_intervalo(self, codigo: str, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os dados históricos de uma ação específica na data fornecida.
        :param codigo: Código da ação (ex.: 'PETR4').
        :param data: Data no formato 'YYYY-MM-DD'.
        :return: Dicionário com os dados da ação na data especificada ou None se não encontrada.
        """
        pass