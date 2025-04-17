from fastapi import FastAPI, File, UploadFile
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from domain.services.process_excel_service import ProcessExcelService
from infrastructure.repositories.bovespa_repository import BovespaRepository
from infrastructure.adapters.cdi_adapter import CDIAdapter
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from application.use_cases.financial_use_case import FinancialUseCase
from infrastructure.adapters.ibov_adapter import IBOVAdapter
from infrastructure.adapters.ibov_adaptee import IBOVAdaptee
from infrastructure.adapters.yfinance_adapter import FinanceAdapter
from infrastructure.adapters.yfinance_adaptee import FinanceAdaptee
from domain.services.financial_service import FinancialService

app = FastAPI()

bovespa_repository = BovespaRepository()
process_excel_service = ProcessExcelService(bovespa_repository)
process_excel_use_case = ProcessExcelUseCase(process_excel_service, bovespa_repository)
financial_use_case = FinancialUseCase(bovespa_repository)

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

@app.post("/cdi-data/")
def post_cdi_data(data_inicial: str, data_final: str):
    cdi_adaptee = CDIAdaptee()
    cdi_adapter = CDIAdapter(cdi_adaptee)
    financial_use_case.cdi_builder(cdi_adapter)
    financial_use_case.post_cdi_data(data_inicial, data_final)

@app.get("/cdi-data/")
def get_cdi_data(data_inicial: str, data_final: str):
    return financial_use_case.get_cdi_data(data_inicial, data_final)

@app.post("/ibov-data/")
async def post_ibov_data(start_date: str, end_date: str):
    ibov_adaptee = IBOVAdaptee()
    ibov_adapter = IBOVAdapter(ibov_adaptee)
    financial_use_case.ibov_builder(ibov_adapter)    
    await financial_use_case.post_ibov_data(start_date, end_date)
    return {"message": "Dados salvos com sucesso"}

@app.get("/ibov-data/")
async def get_ibov_data(start_date: str, end_date: str):
    return financial_use_case.get_ibov_data(start_date, end_date)

@app.post("/acao-data/")
async def post_acao_data(codigo: str, start_date: str, end_date: str):
    finance_adaptee = FinanceAdaptee()
    finance_adapter = FinanceAdapter(finance_adaptee)
    financial_use_case.finance_builder(finance_adapter)    
    await financial_use_case.post_acao_data(codigo, start_date, end_date)
    return {"message": "Dados salvos com sucesso"}

@app.get("/acao-data/")
def get_acao_data(codigo: str, start_date: str, end_date: str):
    return financial_use_case.get_acao_data(codigo, start_date, end_date)

@app.get("/acoes/{codigo}/sharpe")
def calculate_acao_sharpe_ratio(codigo: str, start_date: str, end_date: str):        
    financial_service = FinancialService()
    financial_use_case.financial_service_builder(financial_service)
    result = financial_use_case.calculate_acao_sharpe_ratio(codigo, start_date, end_date)
    return {"message": result}                    