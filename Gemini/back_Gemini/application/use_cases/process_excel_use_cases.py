from domain.services.process_excel_service import ProcessExcelService
from domain.repositories.i_bovespa_repository import IBovespaRepository

class ProcessExcelUseCase:
    def __init__ (self, process_excel_service: ProcessExcelService, bovespa_repository: IBovespaRepository):
        self.process_excel_service = process_excel_service
        self.bovespa_repository = bovespa_repository
    async def process_excel_useCase(self, file: any):        
        segmentos_economico = await self.process_excel_service.get_segmento_economico(file)
        for segmento_data in segmentos_economico:
            sigla = segmento_data.get('Sigla')
            descritivo = segmento_data.get('Descritivo')
            if sigla and descritivo:
                self.bovespa_repository.create_segmentos_economicos(sigla, descritivo)
                print("-----------------------------------")
                print(sigla)
                print(descritivo)
        return "Dados cadastrados com sucesso"