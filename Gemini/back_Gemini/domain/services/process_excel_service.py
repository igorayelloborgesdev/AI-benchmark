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

    async def ler_e_salvar_subsetores(self, file):
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))

            subsetores_a_inserir = []
            for index, row in df.iloc[7:509].iterrows():  # Seleciona as linhas de 9 a 509 (indexação baseada em 0)
                cell_value = row.iloc[1]  # Coluna B tem índice 1 no Pandas

                if pd.notna(cell_value) and str(cell_value).strip() and str(cell_value).strip().upper() != "SUBSETOR":
                    subsetores_a_inserir.append(str(cell_value).strip())

            return subsetores_a_inserir

        except FileNotFoundError:
            print(f"Erro: O arquivo '{file}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def ler_e_salvar_setores_economicos(self, file):
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            setores_a_inserir = []
            for index, row in df.iloc[7:509].iterrows():  # Seleciona as linhas de 9 a 509 (indexação baseada em 0)
                cell_value = row.iloc[0]  # Coluna A tem índice 0 no Pandas

                if pd.notna(cell_value) and str(cell_value).strip() and str(cell_value).strip().upper() != "SETOR ECONÔMICO":
                    setores_a_inserir.append(str(cell_value).strip())

            return setores_a_inserir
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def ler_e_salvar_segmentos(self, file):
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))

            segmentos_a_inserir = []
            for index, row in df.iloc[7:520].iterrows():  # Seleciona as linhas de 8 a 520 (indexação baseada em 0)
                coluna_c_value = row.iloc[2]  # Coluna C tem índice 2 no Pandas
                coluna_d_value = row.iloc[3]  # Coluna D tem índice 3 no Pandas

                if pd.notna(coluna_c_value) and str(coluna_c_value).strip().upper() != "SEGMENTO" and pd.isna(coluna_d_value):
                    segmentos_a_inserir.append(str(coluna_c_value).strip())

            return segmentos_a_inserir

        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")