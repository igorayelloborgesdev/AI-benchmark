from fastapi import UploadFile, HTTPException
import pandas as pd
import re
import io

class ExcelProcessorService:
    """Serviço para processar arquivos Excel e extrair os dados necessários."""

    @staticmethod
    def processar_dados(excel_file: UploadFile, coluna: int = 0, linha_inicial: int = 0, linha_final: int = 0):
        """Lê os dados da planilha e retorna uma lista de dicionários prontos para inserção no banco."""        
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(io.BytesIO(excel_file.file.read()), sheet_name=0, header=None)
            # Selecionar apenas a coluna A (índice 0) e linhas de 521 a 529 (ajustando índice para zero-based)
            dados = df.iloc[linha_inicial - 1:linha_final, coluna].dropna()            
            resultado = []
            for valor in dados:
                match = re.match(r"\((.*?)\)\s*(.*)", str(valor))
                if match:
                    sigla = match.group(1)  # O que está dentro dos parênteses
                    descritivo = match.group(2)  # O que vem depois do parênteses
                    resultado.append({"sigla": sigla, "descritivo": descritivo})
            return resultado

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o Excel: {str(e)}")