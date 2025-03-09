from fastapi import FastAPI, UploadFile, File, Depends
from application.use_cases.process_excel_usecase import ProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from infrastructure.repositories.segmento_classificacao_repository import SegmentoClassificacaoRepository
from typing import List, Tuple
from application.use_cases.sectors_usecase import SectorsUseCase

app = FastAPI()

# Criando instância do serviço e do caso de uso
segmento_repository = SegmentoClassificacaoRepository()
excel_service = ExcelProcessorService(segmento_repository)
process_excel_use_case = ProcessExcelUseCase(excel_service, segmento_repository)

@app.get("/")
def read_root():    
    return {"Hello": "World"}

@app.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...),
    use_case: ProcessExcelUseCase = Depends(lambda: process_excel_use_case)):
    """Recebe um arquivo Excel, lê as linhas 521-529 da coluna A e insere no SQL Server."""    
    await use_case.execute(file)

@app.get("/get-segmentos-classificacao/")
async def getSegmentosClassificacao():        
    sectorsUseCase = SectorsUseCase(segmento_repository)    
    return await sectorsUseCase.get_all_segmento_classificacao()

@app.get("/get-all-setor-economico/")
async def getAllSetorEconomico():        
    sectorsUseCase = SectorsUseCase(segmento_repository)    
    return await sectorsUseCase.get_all_setor_economico()

@app.get("/get-all-subsetor/")
async def getAllSubsetor():        
    sectorsUseCase = SectorsUseCase(segmento_repository)    
    return await sectorsUseCase.get_all_subsetor()

@app.get("/get-all-segmento/")
async def getAllSegmento():        
    sectorsUseCase = SectorsUseCase(segmento_repository)    
    return await sectorsUseCase.get_all_segmento()

