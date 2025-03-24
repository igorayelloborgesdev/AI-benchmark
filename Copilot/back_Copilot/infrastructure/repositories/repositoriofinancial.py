from domain.repositories.i_repositorio_financial import IRepositorioFinancial
from decouple import config
import pyodbc
from typing import List, Dict, Optional
from datetime import datetime

class CDIRepository(IRepositorioFinancial):
    def __init__(self):
        # Lendo variáveis do arquivo .env
        driver = config("DB_DRIVER")
        server = config("DB_SERVER")
        database = config("DB_DATABASE")
        user = config("DB_USER")
        password = config("DB_PASSWORD")

        # Montando a string de conexão
        self.conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
        )

    def salvar_cdi_diario(self, dados: List[Dict]):
        """
        Insere os dados na tabela CDI_Diario.
        """
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for dado in dados:
                # Converter a data para o formato ISO (yyyy-MM-dd)
                data_formatada = datetime.strptime(dado["data"], "%d/%m/%Y").strftime("%Y-%m-%d")
                cursor.execute(
                    """
                    INSERT INTO CDI_Diario (Data, Valor)
                    VALUES (?, ?)
                    """,
                    data_formatada, float(dado["valor"])  # Certifica-se de que o valor seja float
                )
            conn.commit()

    def get_cdi_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os registros da tabela CDI_Diario filtrados pelo intervalo de datas.
        
        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        """
        query = """
        SELECT Data, Valor 
        FROM CDI_Diario
        WHERE Data BETWEEN ? AND ?
        ORDER BY Data
        """        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, data_inicial, data_final)
            rows = cursor.fetchall()

        # Converter os resultados em uma lista de dicionários
        return [{"Data": row.Data.strftime("%Y-%m-%d"), "Valor": row.Valor} for row in rows]

    def salvar_dados(self, dados: List[Dict]):
        """
        Insere os dados na tabela IBovespa_Dados.
        """
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for dado in dados:
                cursor.execute(
                    """
                    INSERT INTO IBOV_Historico (Data, Abertura, Alta, Baixa, Fechamento, Volume)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    dado["Data"], dado["Abertura"], dado["Alta"],
                    dado["Baixa"], dado["Fechamento"], dado["Volume"]
                )
            conn.commit()

    def get_ibov_historico_por_intervalo(self, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os registros do IBOV_Historico filtrados pelo intervalo de datas.

        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        """
        query = """
        SELECT Data, Abertura, Alta, Baixa, Fechamento, Volume
        FROM IBOV_Historico
        WHERE Data BETWEEN ? AND ?
        ORDER BY Data
        """
        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, data_inicial, data_final)
            rows = cursor.fetchall()

        # Converter os resultados em uma lista de dicionários
        return [
            {
                "Data": row.Data.strftime("%Y-%m-%d"),
                "Abertura": row.Abertura,
                "Alta": row.Alta,
                "Baixa": row.Baixa,
                "Fechamento": row.Fechamento,
                "Volume": row.Volume,
            }
            for row in rows
        ]
    
    def salvar_dados_acoes(self, dados: List[Dict]):
        """
        Insere os dados das ações na tabela Acoes_Bovespa.
        """
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            for dado in dados:
                cursor.execute(
                    """
                    INSERT INTO Acao_Historico (Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    dado["Data"], dado["Codigo"], dado["Abertura"], dado["Alta"],
                    dado["Baixa"], dado["Fechamento"], dado["Volume"]
                )
            conn.commit()

    def get_historico_por_acao_e_intervalo(self, codigo: str, data_inicial: str, data_final: str) -> List[Dict]:
        """
        Retorna os dados históricos de uma ação específica filtrados por intervalo de datas.
        :param codigo: Código da ação (ex.: 'PETR4').
        :param data_inicial: Data inicial no formato 'YYYY-MM-DD'.
        :param data_final: Data final no formato 'YYYY-MM-DD'.
        :return: Lista de dicionários com os dados da ação no intervalo especificado.
        """
        query = """
        SELECT Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume
        FROM Acao_Historico
        WHERE Codigo = ? AND Data BETWEEN ? AND ?
        ORDER BY Data
        """        
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, codigo, data_inicial, data_final)
            rows = cursor.fetchall()        
        # Converter os resultados em uma lista de dicionários
        return [
            {
                "Data": row.Data.strftime("%Y-%m-%d"),
                "Codigo": row.Codigo,
                "Abertura": row.Abertura,
                "Alta": row.Alta,
                "Baixa": row.Baixa,
                "Fechamento": row.Fechamento,
                "Volume": row.Volume,
            }
            for row in rows
        ]