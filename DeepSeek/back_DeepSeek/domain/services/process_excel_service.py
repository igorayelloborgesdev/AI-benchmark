import pandas as pd
from typing import List
from domain.repositories.i_bovespa_data_repository import ISegmentoRepository

class ProcessExcelService:
     def __init__(self, segmento_repository: ISegmentoRepository):
         self.segmento_repository = segmento_repository

     def get_segmento_economico(self, file_path: str):
        # Ler o arquivo Excel
        df = pd.read_excel(file_path, header=None)
        
        # Extrair linhas 521 a 529 (considerando que a primeira linha é 0 no pandas)
        rows = df.iloc[520:529, 0].tolist()
        
        segmentos = []
        for row in rows:
            if pd.isna(row):
                continue
                
            # Processar o formato (DR1) BDR Nível 1
            if '(' in row and ')' in row:
                sigla = row.split('(')[1].split(')')[0].strip()
                descritivo = row.split(')')[1].strip()
                
                segmento =  {
                    "sigla": sigla,
                    "descritivo": descritivo
                }
                segmentos.append(segmento)        
        
        return segmentos
     
     def get_sub_setor(self, file_path: str):
         # Ler o arquivo Excel
        df = pd.read_excel(file_path, header=None)
        
        # Extrair linhas 9 a 509 da coluna B (índice 1)
        rows = df.iloc[8:509, 1].tolist()
        
        subsetores = []
        for row in rows:
            # Verificar se é válido (não vazio e diferente de "SUBSETOR")
            if pd.notna(row) and str(row).strip().upper() != "SUBSETOR":
                descritivo = str(row).strip()
                
                # Criar objeto de domínio                
                subsetor =  {                    
                    "descritivo": descritivo
                }
                subsetores.append(subsetor)        
        return subsetores
     
     def get_setor_economico(self, file_path: str):
         # Ler o arquivo Excel
        df = pd.read_excel(file_path, header=None)
        
        # Extrair linhas 9 a 509 da coluna A (índice 0)
        rows = df.iloc[8:509, 0].tolist()
        
        setores = []
        for row in rows:
            # Verificar se é válido (não vazio e diferente de "SETOR ECONÔMICO")
            if pd.notna(row) and str(row).strip().upper() != "SETOR ECONÔMICO":
                descritivo = str(row).strip()
                
                # Criar objeto de domínio                
                setor = {                    
                    "descritivo": descritivo
                }
                setores.append(setor)
        
        # Salvar no banco de dados
        return setores
     
     def get_segmento(self, file_path: str):
          # Ler o arquivo Excel
        df = pd.read_excel(file_path, header=None)
        
        # Extrair linhas 8 a 520 das colunas C (índice 2) e D (índice 3)
        coluna_c = df.iloc[7:520, 2].tolist()
        coluna_d = df.iloc[7:520, 3].tolist()
        
        segmentos = []
        for c_value, d_value in zip(coluna_c, coluna_d):
            # Verificar condições: não pode ser 'SEGMENTO', não pode ser vazio, e coluna D deve estar vazia
            if (pd.notna(c_value) and 
                str(c_value).strip().upper() != "SEGMENTO" and 
                (pd.isna(d_value) or str(d_value).strip() == "")):
                
                descritivo = str(c_value).strip()
                
                # Criar objeto de domínio                
                segmento =  {                    
                    "descritivo": descritivo
                }
                segmentos.append(segmento)
        
        # Salvar no banco de dados
        return segmentos
     
     def get_empresas(self, file_path: str):
        df = pd.read_excel(file_path, header=None)
        
        empresas = []
        current_setor = None
        current_subsetor = None
        current_segmento = None
        
        for index in range(7, 520):  # Linhas 8 a 520
            # Obter valores das colunas
            col_a = df.iloc[index, 0]  # Setor Econômico
            col_b = df.iloc[index, 1]  # Subsetor
            col_c = df.iloc[index, 2]  # Segmento/Nome Empresa
            col_d = df.iloc[index, 3]  # Código
            col_e = df.iloc[index, 4]  # Segmento Classificação
            
            # Atualizar hierarquia
            if pd.notna(col_a) and str(col_a).strip().upper() != "SETOR ECONÔMICO":
                current_setor = str(col_a).strip()
            
            if pd.notna(col_b) and str(col_b).strip().upper() != "SUBSETOR":
                current_subsetor = str(col_b).strip()
            
            if pd.notna(col_c) and str(col_c).strip().upper() != "SEGMENTO" and (pd.isna(col_d) or str(col_d).strip() == ""):
                current_segmento = str(col_c).strip()
            
            # Verificar se é uma linha de empresa
            if (pd.notna(col_c) and 
                str(col_c).strip().upper() != "SEGMENTO" and 
                pd.notna(col_d) and 
                str(col_d).strip() != "" and
                current_setor is not None and
                current_subsetor is not None and
                current_segmento is not None):
                
                # Obter IDs das FKs
                setor_id = self.segmento_repository.get_setor_economico_id_by_descritivo(current_setor)
                subsetor_id = self.segmento_repository.get_subsetor_id_by_descritivo(current_subsetor)
                segmento_id = self.segmento_repository.get_segmento_id_by_descritivo(current_segmento)
                
                # Tratar SegmentoClassificacao (opcional)
                segmento_classificacao_id = None
                if pd.notna(col_e) and str(col_e).strip() != "":
                    segmento_classificacao_id = self.segmento_repository.get_segmento_classificacao_id_by_sigla(str(col_e).strip())
                
                empresa = {
                    "nome": str(col_c).strip(),
                    "codigo": str(col_d).strip(),
                    "segmento_classificacao_id": segmento_classificacao_id,
                    "setor_economico_id": setor_id,
                    "subsetor_id": subsetor_id,
                    "segmento_id": segmento_id
                }                    

                empresas.append(empresa)
        
        return empresas