from fastapi import FastAPI, UploadFile, HTTPException
from application.use_cases.upload_excel_usecase import ProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from infrastructure.repositories.repositoriosql import RepositorioSQL

app = FastAPI()

repositorio_sql = RepositorioSQL()
excel_service = ExcelProcessorService(repositorio_sql)

@app.post("/upload_excel/")
async def upload_excel(file: UploadFile):
    try:
        process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
        await process_excel_usecase.upload_excel(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/segmentos-classificacao")
def get_all_segmento_classificacao():
    process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
    return process_excel_usecase.get_all_segmento_classificacao()

@app.get("/segmentos")
def get_segmentos():
    process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
    return process_excel_usecase.get_segmentos()

@app.get("/setor-economico")
def get_setor_economico():
    process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
    return process_excel_usecase.get_setor_economico()

@app.get("/sub-setor")
def get_sub_setor():    
    process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
    return process_excel_usecase.get_sub_setor()

@app.get("/empresas/{codigo}")
def get_empresa_by_codigo(codigo: str):
    """
    Retorna os dados de uma empresa específica pelo código.
    """
    process_excel_usecase = ProcessExcelUseCase(excel_service, repositorio_sql)
    empresa = process_excel_usecase.get_empresa_by_codigo(codigo)
    
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    return empresa