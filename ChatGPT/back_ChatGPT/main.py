from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from application.use_cases.ExcelProcessorUseCase import ExcelProcessorUseCase
from infrastructure.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repositories.segmento_classificacao_repository import SegmentoClassificacaoRepository

app = FastAPI()

@app.get("/")
def read_root():    
    return {"Hello": "World"}

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)): 
    repository = SegmentoClassificacaoRepository(db)   
    excel_processor = ExcelProcessorUseCase(repository)
    await excel_processor.processar_dados(file)    
    return {"TESTE"}