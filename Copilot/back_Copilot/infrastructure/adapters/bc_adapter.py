from typing import List, Dict
from infrastructure.adapters.bc_adaptee import BCAdaptee
from infrastructure.adapters.i_bc_adapter import IBCAdapter

class BCAdapter(IBCAdapter):
    # """Adapter para consumir a API do Banco Central do Brasil e retornar os dados estruturados."""
    def __init__(self, bc_adaptee: BCAdaptee):
        self.bc_adaptee = bc_adaptee
    
    async def getRequest(self) -> List[Dict]:                
        return await self.bc_adaptee.fetch_cdi_data()
