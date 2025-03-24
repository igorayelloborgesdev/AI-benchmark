from infrastructure.adapters.bc_adapter import BCAdapter
from infrastructure.adapters.ibovespa_adapter import IBovespaAdapter
from infrastructure.adapters.yfinance_adapter import YFinanceAdapter
from domain.repositories.i_repositorio_financial import IRepositorioFinancial
from typing import List, Dict

class FinancialUseCase():    
    def __init__(self, bcdapter: BCAdapter, ibovespa_adapter: IBovespaAdapter, yfinance_adapter: YFinanceAdapter, repositorio_financial: IRepositorioFinancial):
        self.bcdapter = bcdapter
        self.ibovespa_adapter = ibovespa_adapter
        self.yfinance_adapter = yfinance_adapter
        self.repositorio_financial = repositorio_financial                
    async def processar_cdi(self):
        """
        Consome os dados da API e salva na tabela CDI_Diario.
        """
        # Consumir os dados da API do Banco Central
        dados = await self.bcdapter.getRequest()
        # Formatar os dados (ajusta o formato da data, por exemplo)
        dados_formatados = [
            {"data": dado["data"], "valor": float(dado["valor"])}
            for dado in dados
        ]
        # Salvar no banco
        self.repositorio_financial.salvar_cdi_diario(dados_formatados)        

    def get_cdi_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        return self.repositorio_financial.get_cdi_por_intervalo(data_inicial, data_final)        
        
    def consultar_e_salvar_ibovespa(self, start_date: str, end_date: str):
        """
        Consulta os dados do IBovespa e os salva no banco.
        :param start_date: Data inicial no formato 'YYYY-MM-DD'.
        :param end_date: Data final no formato 'YYYY-MM-DD'.
        """
        # Consultar dados do YFinance
        dados = self.ibovespa_adapter.getRequest(start_date, end_date)
        
        # Salvar no banco de dados
        self.repositorio_financial.salvar_dados(dados)

    def get_ibov_historico_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os registros do IBOV_Historico filtrados pelo intervalo de datas.

        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        """
        # Obter os registros do repositório        
        resultados = self.repositorio_financial.get_ibov_historico_por_intervalo(data_inicial, data_final)
        return resultados
    
    def consultar_e_salvar_acoes(self, codigo: str, start_date: str, end_date: str):
        """
        Consulta os dados históricos de uma ação listada na Bovespa e os salva no banco de dados.
        """
        # Consultar dados no YFinance
        dados = self.yfinance_adapter.getRequest(codigo, start_date, end_date)

        # Salvar os dados no banco
        self.repositorio_financial.salvar_dados_acoes(dados)

    def get_historico_por_acao_e_intervalo(self, codigo: str, start_date: str, end_date: str):    
        # Obter os registros do repositório
        resultados = self.repositorio_financial.get_historico_por_acao_e_intervalo(codigo, start_date, end_date)
        return resultados