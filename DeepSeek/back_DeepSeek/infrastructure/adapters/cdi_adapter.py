from typing import List, Dict
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from infrastructure.adapters.i_cdi_adapter import ICDIAdapter
from typing import Optional
from datetime import date

class CDIAdapter(ICDIAdapter):
    # """Adapter para consumir a API do Banco Central do Brasil e retornar os dados estruturados."""
    def __init__(self, cdi_adaptee: CDIAdaptee):
        self.cdi_adaptee = cdi_adaptee
    
    async def getRequest(self, data_inicial: Optional[date] = None, data_final: Optional[date] = None) -> List[Dict]:                
        return await self.cdi_adaptee.fetch_cdi_data(data_inicial, data_final)
