from typing import List, Tuple, Optional
from infrastructure.adapters.bc_adapter import BCAdapter
from domain.repositories.i_finance_repository import IFinanceRepository

class FinancialUseCase():
    """Caso de uso para buscar e salvar os dados do CDI diário."""

    def __init__(self, bc_adapter: BCAdapter, cdi_repository: IFinanceRepository):
        self.bc_adapter = bc_adapter                
        self.cdi_repository = cdi_repository

    async def processcdidata(self) -> int:
        """Executa o processo de buscar e armazenar os dados do CDI."""        
        data = await self.bc_adapter.getRequest()        
        formatted_data: List[Tuple[str, float]] = [
            (entry["data"], float(entry["valor"])) for entry in data
        ]        
        return self.cdi_repository.insert_cdi_data(formatted_data)
    
    async def getcdidiariobydate(self, data_inicial: Optional[str], data_final: Optional[str]) -> List[Tuple[str, float]]:
        """
        Obtém os dados do CDI com filtro opcional de data inicial e final.
        """        
        return self.cdi_repository.get_cdi_data(data_inicial, data_final)

    
