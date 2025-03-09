from typing import List, Tuple
from domain.repositories.i_segmento_classificacao_repository import ISegmentoClassificacaoRepository

class SectorsUseCase():
    """Caso de uso para processar arquivos Excel."""
    def __init__(self, repository: ISegmentoClassificacaoRepository):        
        self.repository = repository  # Adicionamos o repositório como dependência                

    async def get_all_segmento_classificacao(self) -> List[Tuple[int, str, str]]:        
        return self.repository.get_all_segmento_classificacao()
    
    async def get_all_setor_economico(self) -> List[Tuple[int, str]]:        
        return self.repository.get_all_setor_economico()
    
    async def get_all_subsetor(self) -> List[Tuple[int, str]]:        
        return self.repository.get_all_subsetor()
    
    async def get_all_segmento(self) -> List[Tuple[int, str]]:        
        return self.repository.get_all_segmento()
    
    