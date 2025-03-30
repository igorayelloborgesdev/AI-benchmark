from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from application.use_cases.process_excel_use_cases import ProcessExcelUseCase
from domain.services.process_excel_service import ProcessExcelService
from infrastructure.repositories.bovespa_data_repository import PyODBCSegmentoRepository
from application.use_cases.financial_use_case import FinancialUseCase
from infrastructure.adapters.cdi_adaptee import CDIAdaptee
from infrastructure.adapters.cdi_adapter import CDIAdapter
from fastapi import Query
from typing import Optional
from datetime import date
from infrastructure.repositories.financial_repository import FinancialRepository
from infrastructure.adapters.ibov_adaptee import IBOVAdaptee
from infrastructure.adapters.ibov_adapter import IBOVAdapter

app = FastAPI()
segmento_repository = PyODBCSegmentoRepository()
financial_repository = FinancialRepository()
cdi_adaptee = CDIAdaptee()
cdi_adapter = CDIAdapter(cdi_adaptee)
ibov_adaptee = IBOVAdaptee()
ibov_adapter = IBOVAdapter(ibov_adaptee)

@app.post("/upload-segmentos/")
async def upload_segmentos(
    file: UploadFile = File(...)    
):
    try:
        # Salvar o arquivo temporariamente
        file_path = f"temp_{uuid.uuid4()}.xlsx"
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # # Processar o arquivo        
        process_excel_service = ProcessExcelService(segmento_repository)
        use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
        result = use_case.process_excel_useCase(file_path)
        
        # # Remover o arquivo temporário
        os.remove(file_path)
        
        return result
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Erro ao processar arquivo: {str(e)}"}
        )

@app.get("/segmentos_economicos/")
async def get_segmentos_economicos():
    process_excel_service = ProcessExcelService(segmento_repository)
    use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
    segmento_service = use_case.get_segmentos_economicos()    
    return segmento_service

@app.get("/subsetores/")
async def get_subsetores():
    process_excel_service = ProcessExcelService(segmento_repository)
    use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
    subsetores_service = use_case.get_subsetores()    
    return subsetores_service

@app.get("/setores/")
async def get_setores():
    process_excel_service = ProcessExcelService(segmento_repository)
    use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
    setores_service = use_case.get_setores()    
    return setores_service

@app.get("/segmentos/")
async def get_segmentos():
    process_excel_service = ProcessExcelService(segmento_repository)
    use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
    setores_service = use_case.get_segmentos()    
    return setores_service

@app.get("/empresas/{codigo}/")
async def get_empresa_by_codigo(codigo: str):
    try:
        process_excel_service = ProcessExcelService(segmento_repository)
        use_case = ProcessExcelUseCase(process_excel_service, segmento_repository)
        empresas = use_case.get_empresa_by_codigo(codigo)    
        if not empresas:
            raise HTTPException(
                status_code=404,
                detail=f"Empresa com código {codigo} não encontrada"
            )        
        return empresas
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar empresa: {str(e)}"
        )    
    
@app.post("/cdi/atualizar/")
async def atualizar_cdi( data_inicial: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    data_final: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD")):
    financial_use_case = FinancialUseCase(cdi_adapter, ibov_adapter, financial_repository)
    result = await financial_use_case.execute_fetch_and_store(data_inicial, data_final)
    if "error" in result:
        return JSONResponse(
            status_code=500,
            content=result
        )
    return result

@app.get("/cdi/historico/")
def get_cdi_historico(
    data_inicial: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    data_final: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD")    
):
    try:
        financial_use_case = FinancialUseCase(cdi_adapter, ibov_adapter, financial_repository)
        cdis = financial_use_case.execute_get_cdis_by_date_range(data_inicial, data_final)
        return {
            "data": cdis,
            "filtros": {
                "data_inicial": data_inicial.isoformat() if data_inicial else None,
                "data_final": data_final.isoformat() if data_final else None
            },
            "total_registros": len(cdis)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Erro ao consultar CDI: {str(e)}"}
        )
    
@app.post("/ibov/fetch/")
async def fetch_ibov_data(
    start_date: date = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    end_date: date = Query(..., description="Data final no formato YYYY-MM-DD")    
):
    try:
        financial_use_case = FinancialUseCase(cdi_adapter, ibov_adapter, financial_repository)
        total_fetched, total_saved = await financial_use_case.fetch_ibov_data(start_date, end_date)
        return {
            "success": True,
            "message": "Dados do IBOV atualizados com sucesso",
            "total_fetched": total_fetched,
            "total_saved": total_saved
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )    
    
@app.get("/ibov/historico/")
async def get_historical_data(
    start_date: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD"),    
):
    try:
        # Validação adicional de datas
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Data inicial não pode ser maior que data final"
            )
        financial_use_case = FinancialUseCase(cdi_adapter, ibov_adapter, financial_repository)
        return financial_use_case.get_historical_data(start_date, end_date)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar dados: {str(e)}"
        )