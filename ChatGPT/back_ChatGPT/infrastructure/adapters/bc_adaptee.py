import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../../core/.env')
load_dotenv(dotenv_path=dotenv_path)

class BCAdaptee():
    BASE_URL = os.getenv('CDI_DIARIO_URL')
    async def fetch_cdi_data(self) -> List[Dict]:
        """Faz a requisição e retorna os dados do CDI diário."""                
        response = requests.get(self.BASE_URL)                                
        if response.status_code == 200:
            return response.json()  # Retorna os dados em formato de lista de dicionários
        raise Exception(f"Erro ao buscar dados do Banco Central: {response.status_code}")