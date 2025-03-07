from fastapi import UploadFile, HTTPException
from typing import List, Tuple
from application.interfaces.i_process_excel_usecase import IProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from domain.repositories.i_segmento_classificacao_repository import ISegmentoClassificacaoRepository

class ProcessExcelUseCase(IProcessExcelUseCase):
    """Caso de uso para processar arquivos Excel."""
    def __init__(self, excel_service: ExcelProcessorService, repository: ISegmentoClassificacaoRepository):
        self.excel_service = excel_service
        self.repository = repository  # Adicionamos o repositório como dependência

    async def execute(self, file: UploadFile) -> List[Tuple[str, str]]:
        """Executa a lógica de processamento chamando o serviço."""        
        df = await self.excel_service.get_dataframe(file)
        setorLista = await self.excel_service.process_excel(df)
        
        if not setorLista:
            raise HTTPException(status_code=400, detail="Nenhum dado válido encontrado no arquivo.")

        # # Insere os dados no banco usando o repositório
        # self.repository.insert_many(setorLista['segmento'])
        # self.repository.insert_many_setor_economico(setorLista['setor_economico'])
        # self.repository.insert_many_subsetor(setorLista['subsetor'])
        # self.repository.insert_many_segmento_economico(setorLista['segmento_economico'])

        empresas = await self.excel_service.extract_empresas(df)
        print(empresas)

