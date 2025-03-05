from fastapi import FastAPI, UploadFile, File, Depends
from application.use_cases.process_excel_usecase import ProcessExcelUseCase
from domain.services.excel_processor_service import ExcelProcessorService
from infrastructure.repositories.segmento_classificacao_repository import SegmentoClassificacaoRepository

app = FastAPI()

# Criando instância do serviço e do caso de uso
excel_service = ExcelProcessorService()
segmento_repository = SegmentoClassificacaoRepository()
process_excel_use_case = ProcessExcelUseCase(excel_service, segmento_repository)

@app.get("/")
def read_root():    
    return {"Hello": "World"}

@app.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...),
    use_case: ProcessExcelUseCase = Depends(lambda: process_excel_use_case)):
    """Recebe um arquivo Excel, lê as linhas 521-529 da coluna A e insere no SQL Server."""    
    await use_case.execute(file)