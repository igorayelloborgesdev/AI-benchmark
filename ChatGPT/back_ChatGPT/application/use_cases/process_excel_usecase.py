from fastapi import UploadFile, HTTPException
from typing import List, Tuple
from application.interfaces.i_process_excel_usecase import IProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from domain.repositories.i_segmento_classificacao_repository import ISegmentoClassificacaoRepository

class ProcessExcelUseCase(IProcessExcelUseCase):
    """Caso de uso para processar arquivos Excel."""
    def __init__(self, excel_service: ExcelProcessorService, repository: ISegmentoClassificacaoRepository):        
        self.repository = repository  # Adicionamos o repositório como dependência
        self.excel_service = excel_service

    async def execute(self, file: UploadFile) -> List[Tuple[str, str]]:
        """Executa a lógica de processamento chamando o serviço."""        
        df = await self.excel_service.get_dataframe(file)
        setorLista = await self.excel_service.process_excel(df)
        
        if not setorLista:
            raise HTTPException(status_code=400, detail="Nenhum dado válido encontrado no arquivo.")

        empresas = await self.excel_service.extract_empresas(df)        

