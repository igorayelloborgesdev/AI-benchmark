import yfinance as yf
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
from datetime import date

class FinanceAdaptee():        
    async def fetch_acao_data(self, codigo: str, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:
        try:
            # Adiciona .SA para ações brasileiras no YFinance
            ticker = yf.Ticker(f"{codigo}.SA")
            hist = ticker.history(start=data_inicial, end=data_final, auto_adjust=False)
            data = []                        
            for index, row in hist.iterrows():                
                AcaoHistorico = {
                    "codigo": codigo,
                    "data": index.to_pydatetime(),
                    "abertura": row['Open'],
                    "alta": row['High'],
                    "baixa": row['Low'],
                    "fechamento": row['Close'],
                    "volume": int(row['Volume'])
                }                                             
                data.append(AcaoHistorico)            
            return data            
        except Exception as e:
            raise Exception(f"Erro ao buscar dados da ação {codigo}: {str(e)}")