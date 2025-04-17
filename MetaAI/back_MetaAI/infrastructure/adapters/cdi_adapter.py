from typing import List, Dict
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from infrastructure.adapters.i_cdi_adapter import ICDIAdapter

class CDIAdapter(ICDIAdapter):    
    def __init__(self, cdi_adaptee: CDIAdaptee):
        self.cdi_adaptee = cdi_adaptee
    
    def getRequest(self, data_inicial: str, data_final: str) -> List[Dict]:
        return self.cdi_adaptee.fetch_cdi_data(data_inicial, data_final)
