from fastapi import UploadFile, HTTPException
from application.interfaces import IExcelProcessorUseCase
from domain.services.ExcelProcessorService import ExcelProcessorService
from domain.repositories.segmento_classificacao_repository import ISegmentoClassificacaoRepository

class ExcelProcessorUseCase(IExcelProcessorUseCase.IExcelProcessorUseCase):
    """Implementação do caso de uso para processamento de arquivos Excel."""
    def __init__(self, repository: ISegmentoClassificacaoRepository):
        self.repository = repository

    async def processar_dados(self, excel_file: UploadFile):
        try:
            excelProcessorService = ExcelProcessorService()
            segmentoClassificacao = excelProcessorService.processar_dados(excel_file, 0, 521, 529)
            await self.inserir_segmentos(segmentoClassificacao)
            # Ler o arquivo Excel            
        except Exception as e:            
            raise HTTPException(status_code=500, detail=f"Erro ao processar o Excel: {str(e)}")
        
    async def inserir_segmentos(self, segmentoClassificacao):
        """Método separado para inserção dos segmentos no banco de dados."""
        for item in segmentoClassificacao:
            sigla = item['sigla']
            descritivo = item['descritivo']            
            await self.repository.inserir_segmento(sigla, descritivo)        
