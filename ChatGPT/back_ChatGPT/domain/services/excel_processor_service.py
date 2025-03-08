import pandas as pd
import io
import re
from fastapi import HTTPException, UploadFile
from typing import List, Tuple, Optional
from domain.repositories.i_segmento_classificacao_repository import ISegmentoClassificacaoRepository

class ExcelProcessorService:
    """Serviço para processar arquivos Excel e extrair informações específicas."""
    def __init__(self, repository: ISegmentoClassificacaoRepository):        
        self.repository = repository 

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

    async def get_dataframe(self, file: UploadFile):
        # Lendo o arquivo Excel para um DataFrame
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
        return df

    async def process_excel(self, df: pd.DataFrame):
        """
        Lê um arquivo Excel, extrai os dados da coluna A entre as linhas 521 e 529,
        processa os valores e retorna uma lista de tuplas (Sigla, Descritivo).
        """
        try:            
            segmento = await self.process_excel_segmento(df, 521, 529, 0)
            setor_economico = await self.process_excel_setor_subsetor_segmento(df, 8, 509, 0, 'SETOR ECONÔMICO')
            subsetor = await self.process_excel_setor_subsetor_segmento(df, 8, 509, 1, 'SUBSETOR')
            segmento_economico = await self.process_excel_segmento_economico(df, 8, 520, 2, 3, 'SEGMENTO')

            self.repository.insert_many(segmento)	
            self.repository.insert_many_setor_economico(setor_economico)
            self.repository.insert_many_subsetor(subsetor)
            self.repository.insert_many_segmento_economico(segmento_economico)

            return {
                "segmento": segmento,
                "setor_economico": setor_economico,
                "subsetor": subsetor,
                "segmento_economico": segmento_economico
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
        
    async def process_excel_segmento(self, df, initLine: int, endLine: int, columnId: int):        
        try:
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
        
    async def process_excel_setor_subsetor_segmento(self, df, start_row: int, end_row: int, column_index: int, name_exclude: str) -> List[str]:                
        # Pegando os dados da coluna B (index 1 no Pandas) entre as linhas 9 e 509
        extracted_data = df.iloc[start_row-1:end_row, column_index].dropna().tolist()

        # Filtrando linhas que contenham 'SUBSETOR' ou valores vazios
        valid_data = [str(value).strip() for value in extracted_data if str(value).strip().upper() != name_exclude]

        # Removendo duplicatas mantendo a ordem original
        unique_data = list(dict.fromkeys(valid_data))

        return unique_data     
       
    async def process_excel_segmento_economico(self, df, start_row: int, end_row: int, column_index: int, column_ref: int, name_exclude: str) -> List[str]:
        """Lê um arquivo Excel e retorna os valores únicos da coluna C (Segmento), 
        ignorando 'SEGMENTO' e garantindo que a coluna D esteja vazia."""
                
        # Pegando os dados da coluna C (índice 2) e coluna D (índice 3)
        extracted_data = df.iloc[start_row:end_row, [column_index, column_ref]]  # Lembrando que Pandas é baseado em zero        

        # Filtrando valores:
        # 1. Remover linhas onde a coluna C é "SEGMENTO"
        # 2. Manter apenas linhas onde a coluna D está vazia
        filtered_data = extracted_data[
            (extracted_data.iloc[:, 0].astype(str).str.strip().str.upper() != name_exclude) &             
            (extracted_data.iloc[:, 1].isna() | extracted_data.iloc[:, 1].astype(str).str.strip().eq(""))
        ]

        # Removendo NaN e convertendo para lista de strings únicas mantendo a ordem
        segmentos = filtered_data.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        unique_segmentos = list(dict.fromkeys(segmentos))  # Remover duplicatas mantendo a ordem

        return unique_segmentos

    async def extract_empresas(self, df: pd.DataFrame) -> List[Tuple[str, str, Optional[int], int, int, int]]:
        """Extrai e processa os dados do Excel."""
        empresas = []

        for index in range(7, 520):  # Começa na linha 8 (índice 7)
            nome = str(df.iloc[index, 2]).strip() if pd.notna(df.iloc[index, 2]) else None  # Coluna C
            codigo = str(df.iloc[index, 3]).strip() if pd.notna(df.iloc[index, 3]) else None  # Coluna D

            if nome is None or nome.upper() == "SEGMENTO" or not codigo:
                continue  # Pula linhas inválidas

            segmento_classificacao = str(df.iloc[index, 4]).strip() if pd.notna(df.iloc[index, 4]) else None  # Coluna E
            setor_economico = self.get_nearest_valid_value(df, index, 0, "SETOR ECONÔMICO")  # Coluna A
            subsetor = self.get_nearest_valid_value(df, index, 1, "SUBSETOR")  # Coluna B
            segmento = self.get_nearest_valid_segmento(df, index)  # Coluna C com D vazio

            # Buscar IDs no banco
            segmento_classificacao_id = self.repository.get_segmento_classificacao_id(segmento_classificacao)
            setor_economico_id = self.repository.get_setor_economico_id(setor_economico)
            subsetor_id = self.repository.get_subsetor_id(subsetor)
            segmento_id = self.repository.get_segmento_id(segmento)

            if not setor_economico_id or not subsetor_id or not segmento_id:
                continue  # Se algum ID obrigatório não for encontrado, pula a linha

            empresas.append((nome, codigo, segmento_classificacao_id, setor_economico_id, subsetor_id, segmento_id))
            
        self.repository.insert_many_empresas(empresas)            
        return empresas
    
    def get_nearest_valid_value(self, df: pd.DataFrame, row: int, col: int, exclude_value: str) -> Optional[str]:
        """Obtém o primeiro valor acima da linha atual que seja válido (não nulo e diferente do valor excluído)."""
        for i in range(row, -1, -1):
            value = str(df.iloc[i, col]).strip() if pd.notna(df.iloc[i, col]) else None
            if value and value.upper() != exclude_value:
                return value
        return None

    def get_nearest_valid_segmento(self, df: pd.DataFrame, row: int) -> Optional[str]:
        """Obtém o primeiro valor acima na Coluna C que seja válido e tenha a Coluna D vazia."""
        for i in range(row, -1, -1):
            value_c = str(df.iloc[i, 2]).strip() if pd.notna(df.iloc[i, 2]) else None
            value_d = str(df.iloc[i, 3]).strip() if pd.notna(df.iloc[i, 3]) else None

            if value_c and value_c.upper() != "SEGMENTO" and not value_d:
                return value_c
        return None