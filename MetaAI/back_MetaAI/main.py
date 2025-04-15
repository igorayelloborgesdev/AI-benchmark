from fastapi import FastAPI, File, UploadFile
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from domain.services.process_excel_service import ProcessExcelService
from infrastructure.repositories.bovespa_repository import BovespaRepository

app = FastAPI()

process_excel_service = ProcessExcelService()
bovespa_repository = BovespaRepository()
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