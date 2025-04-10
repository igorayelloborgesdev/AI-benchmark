import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from domain.services.process_excel_service import ProcessExcelService
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from infrastructure.repositories.bovespa_repository import BovespaRepository

app = FastAPI()

# Rota para fazer o upload do arquivo Excel e salvar os dados
@app.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Por favor, envie um arquivo Excel válido.")            
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    await use_case.process_excel_useCase(file)

    try:       
        return {"message": "Dados do Excel processados e salvos com sucesso!"}

    except Exception as e:       
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
    
@app.get("/segmentos-classificacao")
def get_all_segmentos_classifcacao():
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    return use_case.get_all_segmentos_classifcacao()    

@app.get("/subsetores")
def get_all_subsetores():
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    return use_case.get_all_subsetores()    

@app.get("/setores")
def get_all_setores():
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    return use_case.get_all_setores()    

@app.get("/segmentos")
def get_all_segmentos():
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    return use_case.get_all_segmentos()    
