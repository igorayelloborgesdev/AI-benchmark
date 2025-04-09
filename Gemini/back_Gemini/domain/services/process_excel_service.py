import pandas as pd
import re
import io
from fastapi import UploadFile

class ProcessExcelService:
    async def get_segmento_economico(self, file: UploadFile):
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        new_records = []
        for index in range(520, 529):  # Linhas de 521 a 529 (índices de 520 a 528)
            if index in df.index:
                cell_value = df.iloc[index, 0]  # Primeira coluna (Coluna A)
                processed_data = self.process_excel_row(str(cell_value))        
                if processed_data:
                    new_records.append(processed_data)  # Adiciona o dicionário à lista
        return new_records  # Retorna a lista de registros processados
    
    # Função para processar a linha do Excel
    def process_excel_row(self, row_value: str):
        match = re.search(r"\((.*?)\) (.*)", row_value)
        if match:
            sigla = match.group(1)
            descritivo = match.group(2).strip()
            return {"Sigla": sigla, "Descritivo": descritivo}
        return None
