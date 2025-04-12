import pandas as pd
import re
import io
from fastapi import UploadFile

class ProcessExcelService:
    async def get_segmento_economico(self, df):        
        new_records = []
        for index in range(519, 529):  # Linhas de 521 a 529 (índices de 520 a 528)
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

    async def ler_e_salvar_subsetores(self, df):
        try:            
            subsetores_a_inserir = []
            for index, row in df.iloc[7:509].iterrows():  # Seleciona as linhas de 9 a 509 (indexação baseada em 0)
                cell_value = row.iloc[1]  # Coluna B tem índice 1 no Pandas

                if pd.notna(cell_value) and str(cell_value).strip() and str(cell_value).strip().upper() != "SUBSETOR":
                    subsetores_a_inserir.append(str(cell_value).strip())

            return subsetores_a_inserir

        except FileNotFoundError:
            print(f"Erro: O arquivo '{df}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def ler_e_salvar_setores_economicos(self, df):
        try:            
            setores_a_inserir = []
            for index, row in df.iloc[7:509].iterrows():  # Seleciona as linhas de 9 a 509 (indexação baseada em 0)
                cell_value = row.iloc[0]  # Coluna A tem índice 0 no Pandas

                if pd.notna(cell_value) and str(cell_value).strip() and str(cell_value).strip().upper() != "SETOR ECONÔMICO":
                    setores_a_inserir.append(str(cell_value).strip())

            return setores_a_inserir
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def ler_e_salvar_segmentos(self, df):
        try:            
            segmentos_a_inserir = []
            for index, row in df.iloc[7:520].iterrows():  # Seleciona as linhas de 8 a 520 (indexação baseada em 0)
                coluna_c_value = row.iloc[2]  # Coluna C tem índice 2 no Pandas
                coluna_d_value = row.iloc[3]  # Coluna D tem índice 3 no Pandas

                if pd.notna(coluna_c_value) and str(coluna_c_value).strip().upper() != "SEGMENTO" and pd.isna(coluna_d_value):
                    segmentos_a_inserir.append(str(coluna_c_value).strip())

            return segmentos_a_inserir

        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def ler_e_salvar_empresas(self, df):
        try:            
            empresas_a_inserir = []            
            segmento_anterior = None

            for index, row in df.iloc[7:520].iterrows():  # Linhas 8 a 520
                nome = row.iloc[2]  # Coluna C
                codigo = row.iloc[3]  # Coluna D
                segmento_classificacao_sigla = row.iloc[4] if pd.notna(row.iloc[4]) else None # Coluna E

                # Lógica para identificar o Segmento (Coluna C quando Coluna D está vazia)
                segmento_descritivo = None
                segmento_col_d_vazio = pd.isna(codigo)
                if segmento_col_d_vazio and pd.notna(nome) and str(nome).strip().upper() != "SEGMENTO":
                    segmento_descritivo = str(nome).strip()
                    segmento_anterior = segmento_descritivo # Atualiza o valor anterior
                elif not segmento_col_d_vazio and pd.notna(nome) and str(nome).strip().upper() != "SEGMENTO" and segmento_anterior:
                    segmento_descritivo = segmento_anterior # Usa o valor anterior se Coluna D não está vazia

                if pd.notna(nome) and str(nome).strip().upper() != "SEGMENTO" and pd.notna(codigo):
                    # Lógica para Setor Econômico (primeira célula não nula acima na Coluna A)
                    setor_economico_descritivo = None
                    for prev_index in range(index - 1, -1, -1):
                        setor_economico_val = df.iloc[prev_index, 0] # Coluna A
                        if pd.notna(setor_economico_val) and str(setor_economico_val).strip().upper() != "SETOR ECONÔMICO":
                            setor_economico_descritivo = str(setor_economico_val).strip()
                            break
                    if not setor_economico_descritivo:
                        print(f"Aviso: Setor Econômico não encontrado para a linha {index + 8}.")
                        continue

                    # Lógica para Subsetor (primeira célula não nula acima na Coluna B)
                    subsetor_descritivo = None
                    for prev_index in range(index - 1, -1, -1):
                        subsetor_val = df.iloc[prev_index, 1] # Coluna B
                        if pd.notna(subsetor_val) and str(subsetor_val).strip().upper() != "SUBSETOR":
                            subsetor_descritivo = str(subsetor_val).strip()
                            break
                    if not subsetor_descritivo:
                        print(f"Aviso: Subsetor não encontrado para a linha {index + 8}.")
                        continue

                    if not segmento_descritivo:
                        print(f"Aviso: Segmento não encontrado para a linha {index + 8}.")
                        continue

                    empresas_a_inserir.append({
                        "Nome": str(nome).strip(),
                        "Codigo": str(codigo).strip(),
                        "SegmentoClassificacaoSigla": str(segmento_classificacao_sigla).strip() if segmento_classificacao_sigla else None,
                        "SetorEconomicoDescritivo": setor_economico_descritivo,
                        "SubsetorDescritivo": subsetor_descritivo,
                        "SegmentoDescritivo": segmento_descritivo,
                    })
            return empresas_a_inserir
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo Excel: {e}")

    async def get_file_dataframe(self, file: UploadFile):
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        return df