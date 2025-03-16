from fastapi import FastAPI, UploadFile, File, Depends, Query, HTTPException
from application.use_cases.process_excel_usecase import ProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from domain.services.calculo_financeiro_service import CalculoFinanceiroService
from infrastructure.repositories.segmento_classificacao_repository import SegmentoClassificacaoRepository
from typing import Optional
from application.use_cases.sectors_usecase import SectorsUseCase
from application.use_cases.financial_usecase import FinancialUseCase
from application.use_cases.ibovespa_usecase import IBovespaUseCase
from infrastructure.adapters.bc_adapter import BCAdapter
from infrastructure.repositories.finance_repository import FinanceRepository
from infrastructure.adapters.bc_adaptee import BCAdaptee
from infrastructure.adapters.ibovespa_adapter import IBovespaAdapter
from infrastructure.adapters.ibovespa_adaptee import IBovespaAdaptee
from application.use_cases.yfinance_usecase import YFinanceUseCase
from infrastructure.adapters.yfinance_adapter import YFinanceAdapter
from infrastructure.adapters.yfinance_adaptee import YFinanceAdaptee
from application.use_cases.calculos_usecase import CalculoUseCase

app = FastAPI()

# Criando instância do serviço e do caso de uso
segmento_repository = SegmentoClassificacaoRepository()
excel_service = ExcelProcessorService(segmento_repository)
calculo_financeiro_service = CalculoFinanceiroService()
process_excel_use_case = ProcessExcelUseCase(excel_service, segmento_repository)
bc_adaptee = BCAdaptee()
bcadapter = BCAdapter(bc_adaptee)
finance_repository = FinanceRepository()
ibovespa_adaptee = IBovespaAdaptee()
ibovespa_adapter = IBovespaAdapter(ibovespa_adaptee)
yfinance_adaptee = YFinanceAdaptee()
yfinance_adapter = YFinanceAdapter(yfinance_adaptee)

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

@app.get("/process-ibovespa")
async def processibovespa(start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")):        
    """
    Consulta os dados históricos do IBovespa e salva no banco de dados.

    :param start_date: Data inicial no formato YYYY-MM-DD
    :param end_date: Data final no formato YYYY-MM-DD
    :return: Número de registros inseridos
    """
    try:
        ibovespa_usecase = IBovespaUseCase(ibovespa_adapter, finance_repository)
        inserted_records = await ibovespa_usecase.fetch_and_store_ibov_data(start_date, end_date)
        return {"message": "Dados inseridos com sucesso!", "registros_inseridos": inserted_records}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/ibovespa/historico")
def get_ibov_historico(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Consulta os dados históricos do IBovespa dentro de um intervalo de datas.

    :param start_date: Data inicial no formato YYYY-MM-DD
    :param end_date: Data final no formato YYYY-MM-DD
    :return: Lista de registros encontrados
    """
    try:
        ibovespa_usecase = IBovespaUseCase(ibovespa_adapter, finance_repository)
        data = ibovespa_usecase.get_ibov_data(start_date, end_date)
         # Converter para lista de dicionários
        formatted_data = [
            {
                "Data": row[0],
                "Abertura": row[1],
                "Alta": row[2],
                "Baixa": row[3],
                "Fechamento": row[4],
                "Volume": row[5]
            }
            for row in data
        ]        
        return {"data": formatted_data}
    except Exception as e:
        return {"error": str(e)}    
    
@app.post("/acoes/{codigo}/historico")
def fetch_and_save_acao(codigo: str, start_date: str, end_date: str):
    """Consulta e armazena os dados da ação no banco"""    
    yfinanceusecase = YFinanceUseCase(yfinance_adapter, finance_repository)
    registros = yfinanceusecase.fetch_and_save_acao(codigo, start_date, end_date)        
    return {"mensagem": f"{registros} registros inseridos com sucesso"}

@app.get("/acoes/{codigo}/historico")
def get_acao_historico(codigo: str, start_date: str, end_date: str):
    """Consulta os dados da ação no banco"""
    yfinanceusecase = YFinanceUseCase(yfinance_adapter, finance_repository)
    data = yfinanceusecase.get_acoes(codigo, start_date, end_date)
    return {"data": [{"Data": row[0], "Codigo": row[1], "Abertura": row[2], "Alta": row[3], "Baixa": row[4], "Fechamento": row[5], "Volume": row[6]} for row in data]}    


@app.get("/analise_risco/{codigo}")
def calcular_analise_risco(
    codigo: str, 
    data_inicio: str, 
    data_fim: str  
):
    try:
        calculousecase = CalculoUseCase(calculo_financeiro_service, finance_repository)
        result = calculousecase.calcular_analise_risco(codigo, data_inicio, data_fim)
        return {"analise": result}        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))