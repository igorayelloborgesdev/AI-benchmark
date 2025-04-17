import yfinance as yf
from typing import List, Dict
from datetime import date
import pandas as pd

class IBOVAdaptee():        
    async def get_data(self, data_inicial: date, data_final: date) ->  pd.DataFrame:
        try:            
            ibov = yf.Ticker("^BVSP")            
            data = ibov.history(start=data_inicial, end=data_final)
            ibov_data_list = []
            for index, row in data.iterrows():            
                ibov_data = {
                    "Data": index.to_pydatetime().date(),
                    "Abertura": row['Open'],
                    "Alta": row['High'],
                    "Baixa": row['Low'],
                    "Fechamento": row['Close'],
                    "Volume": int(row['Volume']) if pd.notna(row['Volume']) else 0
                }
                ibov_data_list.append(ibov_data)
            return ibov_data_list
        except Exception as e:
            raise Exception(f"Erro ao buscar dados do IBOV: {str(e)}")