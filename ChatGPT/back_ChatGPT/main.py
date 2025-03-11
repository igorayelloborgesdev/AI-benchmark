from fastapi import FastAPI, UploadFile, File, Depends, Query
from application.use_cases.process_excel_usecase import ProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from infrastructure.repositories.segmento_classificacao_repository import SegmentoClassificacaoRepository
from typing import Optional
from application.use_cases.sectors_usecase import SectorsUseCase
from application.use_cases.financial_usecase import FinancialUseCase
from infrastructure.adapters.bc_adapter import BCAdapter
from infrastructure.repositories.finance_repository import FinanceRepository
from infrastructure.adapters.bc_adaptee import BCAdaptee

app = FastAPI()

# Criando instância do serviço e do caso de uso
segmento_repository = SegmentoClassificacaoRepository()
excel_service = ExcelProcessorService(segmento_repository)
process_excel_use_case = ProcessExcelUseCase(excel_service, segmento_repository)
bc_adaptee = BCAdaptee()
bcadapter = BCAdapter(bc_adaptee)
finance_repository = FinanceRepository()

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

@app.get("/get-empresa-by-codigo/")
async def getEmpresaByCodigo(codigo: Optional[str] = Query(None, description="Filtrar empresa pelo código")):        
    sectorsUseCase = SectorsUseCase(segmento_repository)        
    return await sectorsUseCase.get_empresa_by_codigo(codigo)

@app.get("/process-cdi-diario")
async def processcdidata():    
    """Endpoint para buscar e salvar os dados do CDI Diário."""    
    financialUseCase = FinancialUseCase(bcadapter, finance_repository)
    rows_inserted = await financialUseCase.processcdidata()
    return {"message": f"{rows_inserted} registros inseridos com sucesso."}
    
@app.get("/get-cdi-diario-by-date")
async def getcdidiariobydate(
    data_inicial: Optional[str] = Query(None, description="Data inicial no formato yyyy-MM-dd"),
    data_final: Optional[str] = Query(None, description="Data final no formato yyyy-MM-dd")
):
    """
    Retorna os dados do CDI filtrados por um intervalo de datas.
    """    
    financialUseCase = FinancialUseCase(bcadapter, finance_repository)
    result = await financialUseCase.getcdidiariobydate(data_inicial, data_final)    
    return [{"data": data, "valor": valor} for data, valor in result]    