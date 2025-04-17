import httpx
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = os.path.join(os.path.dirname(__file__), '../../core/.env')
load_dotenv(dotenv_path=dotenv_path)

class CDIAdaptee():    
    def __init__(self):
        self.base_url = os.getenv('CDI_DIARIO_URL')

    def fetch_cdi_data(self, data_inicial: str, data_final: str):
        try:                                    
            # Converter a string para um objeto datetime
            data_objeto_i = datetime.strptime(data_inicial, '%Y-%m-%d')
            # Formatar o objeto datetime para o formato desejado
            data_inicial_formatada = data_objeto_i.strftime('%d/%m/%Y')
            # Converter a string para um objeto datetime
            data_objeto_f = datetime.strptime(data_final, '%Y-%m-%d')
            # Formatar o objeto datetime para o formato desejado
            data_final_formatada = data_objeto_f.strftime('%d/%m/%Y')
            url = self.base_url + f"dataInicial={data_inicial_formatada}&dataFinal={data_final_formatada}"
            response = requests.get(url)
            return response.json()
        except requests.RequestException as e:            
            raise Exception(f"Erro ao acessar API do BCB: {str(e)}")