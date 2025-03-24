import yfinance as yf
from typing import List, Dict

class IBovespaAdaptee:

    def get_historical_data(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Consulta dados históricos do IBovespa no YFinance.
        :param start_date: Data inicial no formato 'YYYY-MM-DD'.
        :param end_date: Data final no formato 'YYYY-MM-DD'.
        :return: Lista de dicionários com os dados históricos.
        """
        ticker = "^BVSP"
        ticker_data = yf.Ticker(ticker)
        data = ticker_data.history(start=start_date, end=end_date)
        
        # Formatar os dados
        historical_data = []
        for date, row in data.iterrows():
            historical_data.append({
                "Data": date.strftime("%Y-%m-%d"),
                "Abertura": row["Open"],
                "Alta": row["High"],
                "Baixa": row["Low"],
                "Fechamento": row["Close"],
                "Volume": row["Volume"]
            })
        return historical_data