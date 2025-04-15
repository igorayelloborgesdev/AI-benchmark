from domain.services.process_excel_service import ProcessExcelService
from domain.repositories.i_bovespa_repository import IBovespaRepository

class ProcessExcelUseCase:
   def __init__ (self, process_excel_service: ProcessExcelService, bovespa_repository: IBovespaRepository):
        self.process_excel_service = process_excel_service
        self.bovespa_repository = bovespa_repository
   async def ler_arquivo_excel(self, arquivo_excel):
          segmento_classificacao = await self.process_excel_service.ler_arquivo_excel_segmento_classificacao(arquivo_excel)          
          self.bovespa_repository.create_segmentos_economicos(segmento_classificacao)

   def get_segmentos_classificacao(self):
        return self.bovespa_repository.get_segmentos_classificacao()
          