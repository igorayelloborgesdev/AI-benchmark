import yfinance as yf
from typing import List, Tuple
from datetime import datetime

class YFinanceAdaptee:
    """Adapter para buscar dados de ações na API do Yahoo Finance"""

    def fetch_stock_data(self, ticker: str, start_date: str, end_date: str) -> List[Tuple]:
        """
        Busca os dados históricos de uma ação no Yahoo Finance.
        
        :param ticker: Código da ação (ex: "PETR4.SA")
        :param start_date: Data de início no formato YYYY-MM-DD
        :param end_date: Data de fim no formato YYYY-MM-DD
        :return: Lista de tuplas contendo (Data, Codigo, Abertura, Alta, Baixa, Fechamento, Volume)
        """        
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)        
        if df.empty:
            return []

        data_list = [
            (                
                datetime.strptime(str(date).split()[0], "%Y-%m-%d").date(),  # Remove horas e minutos
                ticker.replace(".SA", ""),  # Remove o ".SA" do código
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"]
            )
            for date, row in df.iterrows()
        ]        
        return data_list
