from fastapi import FastAPI, File, UploadFile
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from domain.services.process_excel_service import ProcessExcelService
from infrastructure.repositories.bovespa_repository import BovespaRepository

app = FastAPI()

bovespa_repository = BovespaRepository()
process_excel_service = ProcessExcelService(bovespa_repository)
process_excel_use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)

@app.post("/segmento-classificacao/")
async def criar_segmento_classificacao(arquivo_excel: UploadFile = File(...)):
    contents = await arquivo_excel.read()
    await process_excel_use_case.ler_arquivo_excel(contents)
    return {"mensagem": "Segmento de classificação criado com sucesso!"}

@app.get("/segmentos-classificacao/")
async def get_segmentos_classificacao():        
    segmentos = process_excel_use_case.get_segmentos_classificacao()
    return segmentos

@app.get("/setores-economicos/")
async def get_setores_economicos():        
    setores = process_excel_use_case.get_setores_economicos()
    return setores

@app.get("/sub-setores/")
async def get_sub_setores():        
    sub_setores = process_excel_use_case.get_sub_setores()
    return sub_setores

@app.get("/get-segmentos/")
async def get_segmentos():        
    segmentos = process_excel_use_case.get_segmentos()
    return segmentos

@app.get("/get-empresa-by-codigo/")
def get_empresa_by_codigo(codigo):
    empresa = process_excel_use_case.get_empresa_by_codigo(codigo)
    return empresa