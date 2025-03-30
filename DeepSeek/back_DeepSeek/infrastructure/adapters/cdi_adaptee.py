import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
from datetime import date

dotenv_path = os.path.join(os.path.dirname(__file__), '../../core/.env')
load_dotenv(dotenv_path=dotenv_path)

class CDIAdaptee():    
    def __init__(self):
        self.base_url = os.getenv('CDI_DIARIO_URL')

    async def fetch_cdi_data(self, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:
        try:            
            # Preparar parâmetros da requisição
            params = {"formato": "json"}
            
            # Adicionar filtros de data se fornecidos
            if data_inicial:
                params["dataInicial"] = data_inicial.strftime('%d/%m/%Y')
            if data_final:
                params["dataFinal"] = data_final.strftime('%d/%m/%Y')
            
            # Fazer a requisição
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()            
            data = response.json()            
            cdis = []            
            for item in data:
                try:
                    cdi = {
                        "data": datetime.strptime(item['data'], '%d/%m/%Y').date(),
                        "valor": float(item['valor'])
                    }
                    cdis.append(cdi)
                except (ValueError, KeyError) as e:
                    continue            
            return cdis
        except requests.RequestException as e:
            raise Exception(f"Erro ao acessar API do BCB: {str(e)}")