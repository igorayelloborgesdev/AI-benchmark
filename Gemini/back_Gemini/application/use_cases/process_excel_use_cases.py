from domain.services.process_excel_service import ProcessExcelService
from domain.repositories.i_bovespa_repository import IBovespaRepository

class ProcessExcelUseCase:
    def __init__ (self, process_excel_service: ProcessExcelService, bovespa_repository: IBovespaRepository):
        self.process_excel_service = process_excel_service
        self.bovespa_repository = bovespa_repository
    async def process_excel_useCase(self, file: any):        
        df = await self.process_excel_service.get_file_dataframe(file)
        segmentos_economico = await self.process_excel_service.get_segmento_economico(df)
        for segmento_data in segmentos_economico:
            sigla = segmento_data.get('Sigla')
            descritivo = segmento_data.get('Descritivo')
            if sigla and descritivo:
                self.bovespa_repository.create_segmentos_economicos(sigla, descritivo)   
        subsetores_a_inserir = await self.process_excel_service.ler_e_salvar_subsetores(df)
        self.bovespa_repository.create_subsetor(subsetores_a_inserir)
        setores_a_inserir  = await self.process_excel_service.ler_e_salvar_setores_economicos(df)
        self.bovespa_repository.create_subsetores(setores_a_inserir)
        segmentos_a_inserir  = await self.process_excel_service.ler_e_salvar_segmentos(df)
        self.bovespa_repository.create_segmentos(segmentos_a_inserir)
        empresas_a_inserir = await self.process_excel_service.ler_e_salvar_empresas(df)
        await self.bovespa_repository.inserir_empresas(empresas_a_inserir)
        return "Dados cadastrados com sucesso"
    
    def get_all_segmentos_classifcacao(self):
        return self.bovespa_repository.get_all_segmentos_classifcacao()
    
    def get_all_subsetores(self):
        return self.bovespa_repository.get_all_subsetores()
    
    def get_all_setores(self):
        return self.bovespa_repository.get_all_setores()
    
    def get_all_segmentos(self):
        return self.bovespa_repository.get_all_segmentos()
    
    async def read_empresa(self, empresa_id: str):
        return await self.bovespa_repository.get_empresa_by_id(empresa_id)