from fastapi import UploadFile
from domain.services.excel_processor_service import ExcelProcessorService
from domain.repositories.i_repositorio_segmento import IRepositorioSegmento

class ProcessExcelUseCase():

    def __init__(self, excel_service: ExcelProcessorService, i_repositorio_segmento: IRepositorioSegmento):        
        self.excel_service = excel_service
        self.i_repositorio_segmento = i_repositorio_segmento

    async def upload_excel(self, data: UploadFile):        
        data = await self.excel_service.upload_excel(data)
        segmento_classificacao = self.excel_service.extrair_segmentos_classificacao(data)
        self.i_repositorio_segmento.salvar_segmento_classificacao(segmento_classificacao)        
        setor_economico = self.excel_service.extrair_setor_economico(data)
        self.i_repositorio_segmento.salvar_setor_economico(setor_economico)                
        sub_setor_economico = self.excel_service.extrair_sub_setor_economico(data)
        self.i_repositorio_segmento.salvar_sub_setor_economico(sub_setor_economico)        
        segmentos = self.excel_service.extrair_segmentos(data)        
        self.i_repositorio_segmento.salvar_segmento(segmentos)        
        empresas = self.excel_service.extrair_dados_empresa(data)                
        self.i_repositorio_segmento.salvar_empresa(empresas)

    def get_all_segmento_classificacao(self):
        return self.i_repositorio_segmento.get_all_segmento_classificacao()
    
    def get_segmentos(self):
        return self.i_repositorio_segmento.get_segmentos()
    
    def get_setor_economico(self):
        return self.i_repositorio_segmento.get_setor_economico()
    
    def get_sub_setor(self):
        return self.i_repositorio_segmento.get_sub_setor()
    
    def get_empresa_by_codigo(self, codigo):
        return self.i_repositorio_segmento.get_empresa_by_codigo(codigo)


    