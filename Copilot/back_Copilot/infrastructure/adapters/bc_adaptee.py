import requests
from typing import List, Dict
from decouple import config

class BCAdaptee():
    def __init__(self):
        # Lendo variáveis do arquivo .env    
        self.base_url = config("CDI_DIARIO_URL")
    async def fetch_cdi_data(self) -> List[Dict]:
        """
        Consome os dados de CDI Diário da API do Banco Central.
        """
        response = requests.get(f"{self.base_url}")
        response.raise_for_status()  # Levanta exceção para status de erro
        return response.json()