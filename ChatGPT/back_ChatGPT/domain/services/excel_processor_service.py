import pandas as pd
import io
import re
from fastapi import HTTPException, UploadFile

class ExcelProcessorService:
    """Serviço para processar arquivos Excel e extrair informações específicas."""

    @staticmethod
    def extract_data_from_text(text: str):
        """
        Extrai a Sigla (dentro dos parênteses) e o Descritivo (após os parênteses).
        Exemplo: "(DR1) BDR Nível 1" -> Sigla: "DR1", Descritivo: "BDR Nível 1"
        """
        match = re.match(r"\((.*?)\)\s*(.*)", text)
        if match:
            sigla = match.group(1)
            descritivo = match.group(2)
            return sigla, descritivo
        return None, None

    async def process_excel(self, file: UploadFile, initLine: int, endLine: int, columnId: int):
        """
        Lê um arquivo Excel, extrai os dados da coluna A entre as linhas 521 e 529,
        processa os valores e retorna uma lista de tuplas (Sigla, Descritivo).
        """
        try:
            # Lendo o arquivo Excel para um DataFrame
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")

            # Pegando os dados da coluna A entre as linhas 521 e 529 (índices base 0)
            extracted_data = df.iloc[initLine:endLine, columnId].dropna().tolist()

            if not extracted_data:
                raise HTTPException(status_code=400, detail="Nenhum dado encontrado no intervalo especificado.")

            # Processar os dados
            processed_data = [self.extract_data_from_text(row) for row in extracted_data if isinstance(row, str)]

            # Filtrar entradas válidas
            valid_data = [(sigla, descritivo) for sigla, descritivo in processed_data if sigla and descritivo]

            if not valid_data:
                raise HTTPException(status_code=400, detail="Nenhuma linha com formato válido encontrada.")
            
            return valid_data

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
