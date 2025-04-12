from typing import List, Dict
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from infrastructure.adapters.i_cdi_adapter import ICDIAdapter

class CDIAdapter(ICDIAdapter):
    # """Adapter para consumir a API do Banco Central do Brasil e retornar os dados estruturados."""
    def __init__(self, cdi_adaptee: CDIAdaptee):
        self.cdi_adaptee = cdi_adaptee
    
    async def getRequest(self, data_inicial: str, data_final: str) -> List[Dict]:
        return await self.cdi_adaptee.fetch_cdi_data(data_inicial, data_final)
