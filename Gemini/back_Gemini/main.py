import httpx
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from domain.services.process_excel_service import ProcessExcelService
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from infrastructure.repositories.bovespa_repository import BovespaRepository
from application.use_cases.financial_use_case import FinancialUseCase
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from infrastructure.adapters.cdi_adapter import CDIAdapter
from datetime import date
from infrastructure.adapters.ibov_adaptee import IBOVAdaptee
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.yfinance_adaptee import FinanceAdaptee
from infrastructure.adapters.yfinance_adapter import FinanceAdapter

app = FastAPI()
cdi_adaptee = CDIAdaptee()
cdi_adapter = CDIAdapter(cdi_adaptee)
ibov_adaptee = IBOVAdaptee()
ibov_adapter = IBOVAdapter(ibov_adaptee)
finance_adaptee = FinanceAdaptee()
finance_adapter = FinanceAdapter(finance_adaptee)

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

@app.get("/empresas/{empresa_id}")
async def read_empresa(empresa_id: str):
    bovespa_repository = BovespaRepository()
    process_excel_service = ProcessExcelService()
    use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
    empresa = await use_case.read_empresa(empresa_id)
    if empresa:
        return empresa
    return {"message": "Empresa não encontrada"}

@app.post("/fetch_and_save_cdi")
async def fetch_and_save_cdi(
    data_inicial: str,
    data_final: str    
):    
    try:
        bovespa_repository = BovespaRepository()
        use_case = FinancialUseCase(cdi_adapter, ibov_adapter, finance_adapter, bovespa_repository)
        result = await use_case.fetch_and_save_cdi(data_inicial, data_final)
        return {"message": result}
    except httpx.HTTPError as e:
        return {"error": f"Error fetching data from BCB API: {e}"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/cdi")
async def read_cdi_by_date_range(
    data_inicial: date,
    data_final: date
):
    """
    Retorna os valores do CDI dentro do intervalo de datas especificado.
    """
    bovespa_repository = BovespaRepository()
    cdi_data = await bovespa_repository.get_cdi_by_date_range(data_inicial, data_final)
    return cdi_data

@app.post("/fetch_and_save_ibov")
async def fetch_and_save_ibov(
    start_date: date,
    end_date: date
):    
    try:
        bovespa_repository = BovespaRepository()
        use_case = FinancialUseCase(cdi_adapter, ibov_adapter, finance_adapter, bovespa_repository)
        result = await use_case.fetch_and_save_ibov(start_date, end_date)
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/ibov_historico")
async def read_ibov_historico_by_date_range(
    data_inicial: date,
    data_final: date,    
):
    """
    Retorna os dados históricos do Ibovespa dentro do intervalo de datas especificado.
    """
    bovespa_repository = BovespaRepository()
    ibov_data = await bovespa_repository.get_ibov_by_date_range(data_inicial, data_final)    
    return ibov_data

@app.post("/baixar_acao/")
async def baixar_acao(
    codigo: str,
    start_date: date,
    end_date: date    
):
    try:
        bovespa_repository = BovespaRepository()
        use_case = FinancialUseCase(cdi_adapter, ibov_adapter, finance_adapter, bovespa_repository)
        result = await use_case.get_ibov_by_date_range(codigo, start_date, end_date)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/acoes/historico")
def read_acao_historico(
    codigo: str = Query(..., description="Código da ação (ex: PETR4)"),
    data_inicial: date = Query(..., description="Data inicial para o filtro (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final para o filtro (YYYY-MM-DD)")
):
    """
    Retorna o histórico de uma ação específica dentro do intervalo de datas.
    """
    bovespa_repository = BovespaRepository()    
    historico = bovespa_repository.get_acao_historico(codigo, data_inicial, data_final)    
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico da ação não encontrado para o período especificado.")
    return historico
