from domain.services.process_excel_service import ProcessExcelService
from domain.repositories.i_bovespa_data_repository import ISegmentoRepository

class ProcessExcelUseCase:
    def __init__ (self, process_excel_service: ProcessExcelService, segmento_repository: ISegmentoRepository):
        self.process_excel_service = process_excel_service
        self.segmento_repository = segmento_repository

    def process_excel_useCase(self, file_path: str):
        segmento = self.process_excel_service.get_segmento_economico(file_path)        
        self.segmento_repository.create_segmentos_economicos(segmento)
        sub_setores = self.process_excel_service.get_sub_setor(file_path)
        self.segmento_repository.create_sub_setor(sub_setores)                
        setor_economico = self.process_excel_service.get_setor_economico(file_path)
        self.segmento_repository.create_setor_economico(setor_economico)                
        setor_economico = self.process_excel_service.get_segmento(file_path)
        self.segmento_repository.create_segmentos(setor_economico) 
        empresas = self.process_excel_service.get_empresas(file_path)        
        self.segmento_repository.create_empresas(empresas)
        return "Dados cadastrados com sucesso"
    
    def get_segmentos_economicos(self):
        return self.segmento_repository.get_segmentos_economicos()
    
    def get_subsetores(self):
        return self.segmento_repository.get_subsetores()
    
    def get_setores(self):
        return self.segmento_repository.get_setores()
    
    def get_segmentos(self):
        return self.segmento_repository.get_segmentos()
    
    def get_empresa_by_codigo(self, codigo: str):
        return self.segmento_repository.get_empresa_by_codigo(codigo)