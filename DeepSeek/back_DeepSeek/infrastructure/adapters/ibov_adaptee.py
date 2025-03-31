import yfinance as yf
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
from datetime import date

class IBOVAdaptee():        
    async def fetch_historical_data(self, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:
        try:            
            # ^BVSP é o ticker do IBovespa no Yahoo Finance
            ibov = yf.Ticker("^BVSP")            
            hist = ibov.history(start=data_inicial, end=data_final)
            data = []
            for index, row in hist.iterrows():
                IBOVDailyData = {
                    "data": index.date(),
                    "abertura": row['Open'],
                    "alta": row['High'],
                    "baixa": row['Low'],
                    "fechamento": row['Close'],
                    "volume": int(row['Volume'])
                }
                                    
                data.append(IBOVDailyData)            
            return data
        except Exception as e:
            raise Exception(f"Erro ao buscar dados do IBOV: {str(e)}")