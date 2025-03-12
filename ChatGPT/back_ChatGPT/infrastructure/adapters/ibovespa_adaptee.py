import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Tuple

class IBovespaAdaptee:
    """Adaptee para consumir dados históricos do IBovespa usando YFinance."""

    async def fetch_ibovespa_data(self, start_date: str, end_date: str) -> List[Tuple[str, float, float, float, float, int]]:
        """
        Busca os dados históricos do IBovespa entre as datas fornecidas.

        :param start_date: Data inicial (YYYY-MM-DD)
        :param end_date: Data final (YYYY-MM-DD)
        :return: Lista de tuplas com os dados (Data, Abertura, Alta, Baixa, Fechamento, Volume)
        """        
        ticker = "^BVSP"        
        ibov = yf.Ticker(ticker)        
        df = ibov.history(start=start_date, end=end_date)        
        if df.empty:
            return []

        return [
            (
                date.strftime("%Y-%m-%d"), 
                row["Open"], 
                row["High"], 
                row["Low"], 
                row["Close"], 
                int(row["Volume"])
            ) 
            for date, row in df.iterrows()
        ]
