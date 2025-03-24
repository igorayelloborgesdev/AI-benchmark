from fastapi import FastAPI, UploadFile, HTTPException, Query
from application.use_cases.upload_excel_usecase import ProcessExcelUseCase
from application.use_cases.financial_usecase import FinancialUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from infrastructure.repositories.repositoriosql import RepositorioSQL
from infrastructure.adapters.bc_adapter import BCAdapter
from infrastructure.adapters.bc_adaptee import BCAdaptee
from infrastructure.repositories.repositoriofinancial import CDIRepository
from infrastructure.adapters.ibovespa_adapter import IBovespaAdapter
from infrastructure.adapters.ibovespa_adaptee import IBovespaAdaptee
from infrastructure.adapters.yfinance_adapter import YFinanceAdapter
from infrastructure.adapters.yfinance_adaptee import YFinanceAdaptee
from datetime import datetime

app = FastAPI()

repositorio_sql = RepositorioSQL()
excel_service = ExcelProcessorService(repositorio_sql)
bc_adaptee = BCAdaptee()
bcadapter = BCAdapter(bc_adaptee)
ibovespa_adaptee = IBovespaAdaptee()
ibovespa_adapter = IBovespaAdapter(ibovespa_adaptee)
yfinance_adaptee = YFinanceAdaptee()
yfinance_adapter = YFinanceAdapter(yfinance_adaptee)
repositorio_cdi = CDIRepository()

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

@app.post("/cdi/diario")
async def processar_cdi():
    """
    Processa e salva os dados do CDI Diário.
    """
    financial_usecase = FinancialUseCase(bcadapter, repositorio_cdi)
    await financial_usecase.processar_cdi()
    return {"message": "Dados processados e salvos com sucesso."}

@app.get("/cdi/diario")
def get_cdi_por_intervalo(
    data_inicial: str = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    data_final: str = Query(..., description="Data final no formato YYYY-MM-DD"),
):
    """
    Consulta os registros de CDI Diário no intervalo de datas fornecido.
    """
    financial_usecase = FinancialUseCase(bcadapter, ibovespa_adapter, yfinance_adapter, repositorio_cdi)
    try:
        # Validar os parâmetros (exemplo básico)
        if not data_inicial or not data_final:
            raise ValueError("Os parâmetros data_inicial e data_final são obrigatórios.")
        
        # Obter os dados filtrados
        resultados = financial_usecase.get_cdi_por_intervalo(data_inicial, data_final)
        
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado no intervalo especificado.")

        return resultados
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/ibovespa/historico")
def consultar_e_salvar_ibovespa(start_date: str, end_date: str):
    """
    Consulta os dados históricos do IBovespa e os salva no banco de dados.
    """
    financial_usecase = FinancialUseCase(bcadapter, ibovespa_adapter, yfinance_adapter, repositorio_cdi)
    try:
        financial_usecase.consultar_e_salvar_ibovespa(start_date, end_date)
        return {"message": "Dados do IBovespa processados e salvos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/ibov/historico")
def get_ibov_historico(
    data_inicial: str = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    data_final: str = Query(..., description="Data final no formato YYYY-MM-DD"),
):
    """
    Consulta os registros do IBOV_Historico no intervalo de datas fornecido.
    """
    financial_usecase = FinancialUseCase(bcadapter, ibovespa_adapter, yfinance_adapter, repositorio_cdi)
    try:
        # Validar os parâmetros básicos
        if not data_inicial or not data_final:
            raise ValueError("As datas inicial e final são obrigatórias.")
        
        # Obter os registros do repositório
        resultados = financial_usecase.get_ibov_historico_por_intervalo(data_inicial, data_final)
        
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado no intervalo especificado.")

        return resultados
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")
    
@app.post("/acoes/historico")
def consultar_e_salvar_acoes(codigo: str, start_date: str, end_date: str):
    """
    Consulta os dados históricos de uma ação listada na Bovespa e os salva no banco de dados.
    """
    financial_usecase = FinancialUseCase(bcadapter, ibovespa_adapter, yfinance_adapter, repositorio_cdi)
    try:
        financial_usecase.consultar_e_salvar_acoes(codigo, start_date, end_date)
        return {"message": f"Dados da ação {codigo} processados e salvos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@app.get("/acoes/historico")
def consultar_e_salvar_acoes(codigo: str, start_date: str, end_date: str):    
    financial_usecase = FinancialUseCase(bcadapter, ibovespa_adapter, yfinance_adapter, repositorio_cdi)
    #Consulta os dados de ações no YFinance e salva no banco de dados.
    
    # Validar o código da ação
    if not codigo or not codigo.endswith(".SA"):
        raise HTTPException(
            status_code=400,
            detail=f"Código inválido: {codigo}. O código deve terminar com '.SA' (ex.: PETR4.SA)."
        )

    # Validar formato e consistência das datas
    try:
        # Converter as datas para objetos datetime
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de data inválido. Use 'YYYY-MM-DD'. Datas recebidas: start_date={start_date}, end_date={end_date}."
        )

    # Verificar consistência das datas
    if start_date_obj > end_date_obj:
        raise HTTPException(
            status_code=400,
            detail=f"A data inicial {start_date} não pode ser maior que a data final {end_date}."
        )
    try:                
        # Obter os registros do repositório
        resultados = financial_usecase.get_historico_por_acao_e_intervalo(codigo, start_date, end_date)
        
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado no intervalo especificado.")

        return resultados
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")