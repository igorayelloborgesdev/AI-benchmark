from domain.services.process_excel_service import ProcessExcelService
from domain.repositories.i_bovespa_repository import IBovespaRepository

class ProcessExcelUseCase:
   def __init__ (self, process_excel_service: ProcessExcelService, bovespa_repository: IBovespaRepository):
        self.process_excel_service = process_excel_service
        self.bovespa_repository = bovespa_repository
   async def ler_arquivo_excel(self, arquivo_excel):
          segmento_classificacao = await self.process_excel_service.ler_arquivo_excel_segmento_classificacao(arquivo_excel)          
          self.bovespa_repository.create_segmentos_economicos(segmento_classificacao)
          segmento_classificacao = await self.process_excel_service.ler_setor_economico(arquivo_excel)          
          self.bovespa_repository.create_setores_economicos(segmento_classificacao)
          sub_setores = await self.process_excel_service.importar_sub_setor(arquivo_excel)
          self.bovespa_repository.create_sub_setores(sub_setores)
          segmentos = await self.process_excel_service.importar_segmento(arquivo_excel)
          self.bovespa_repository.create_segmentos(segmentos)          
          empresas = await self.process_excel_service.importar_empresas(arquivo_excel)
          self.bovespa_repository.create_empresas(empresas)

   def get_segmentos_classificacao(self):
        return self.bovespa_repository.get_segmentos_classificacao()
   
   def get_setores_economicos(self):
        return self.bovespa_repository.get_setores_economicos()
   
   def get_sub_setores(self):
        return self.bovespa_repository.get_sub_setores()
          
   def get_segmentos(self):
        return self.bovespa_repository.get_segmentos()
   
   def get_empresa_by_codigo(self, codigo):
        return self.bovespa_repository.get_empresa_by_codigo(codigo)