import yfinance as yf
from typing import List, Dict

class YFinanceAdaptee:
    def __init__(self):
        pass

    def get_historical_data(self, codigo: str, start_date: str, end_date: str) -> List[Dict]:
        """
        Consulta dados históricos de uma ação no YFinance.
        :param codigo: Código da ação (ex: 'PETR4.SA').
        :param start_date: Data inicial no formato 'YYYY-MM-DD'.
        :param end_date: Data final no formato 'YYYY-MM-DD'.
        :return: Lista de dicionários com os dados históricos.
        """
        ticker_data = yf.Ticker(codigo)
        data = ticker_data.history(start=start_date, end=end_date, auto_adjust=False)

        # Formatar os dados
        historical_data = []
        for date, row in data.iterrows():
            historical_data.append({
                "Data": date.strftime("%Y-%m-%d"),
                "Codigo": codigo,
                "Abertura": row["Open"],
                "Alta": row["High"],
                "Baixa": row["Low"],
                "Fechamento": row["Close"],
                "Volume": row["Volume"]
            })
        return historical_data
