import io
from fastapi import UploadFile
from fastapi import UploadFile, HTTPException
import pandas as pd
from pandas import DataFrame
import re
from domain.repositories.i_repositorio_segmento import IRepositorioSegmento

class ExcelProcessorService:

    def __init__(self, repositorio_segmento: IRepositorioSegmento):
        self.repositorio_segmento = repositorio_segmento

    async def upload_excel(self, file: UploadFile):
        try:
            # Verificar se o arquivo é Excel
            if not file.filename.endswith((".xlsx", ".xls")):
                raise HTTPException(status_code=400, detail="Arquivo inválido. Envie um arquivo Excel.")

            # Ler o conteúdo do arquivo como bytes usando await
            file_content = await file.read()

            # Criar um buffer de memória com o conteúdo do arquivo
            excel_buffer = io.BytesIO(file_content)

            # Ler o arquivo Excel com pandas
            data = pd.read_excel(excel_buffer, header=None)
            return data
            
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def extrair_segmentos_classificacao(self, data: DataFrame):
        selected_data = data.iloc[520:529, 0]  # Selecionar linhas e coluna desejadas
        records = []
        for row in selected_data:
            match = re.match(r"\((.*?)\)\s*(.*)", row)
            if match:
                sigla, descritivo = match.groups()
                records.append({"Sigla": sigla, "Descritivo": descritivo})
        return records
    
    def extrair_setor_economico(self, data: DataFrame):
        """
        Extrai os valores válidos da coluna B, desconsiderando "SETOR ECONÔMICO" e valores em branco.
        """
        # Selecionar os dados da coluna A (ignora as primeiras 8 linhas)
        selected_data = data.iloc[8:509, 0]  # Índices baseados em zero (coluna A -> índice 0)
        records = []

        # Processar os dados
        for row in selected_data:
            if pd.isna(row) or "SETOR ECONÔMICO" in str(row):  # Ignorar valores nulos ou "SETOR ECONÔMICO"
                continue
            records.append({"Descritivo": row.strip()})  # Adiciona o valor formatado

        return records        

    def extrair_sub_setor_economico(self, data: DataFrame):
        """
        Extrai os valores válidos da coluna B, desconsiderando "SUBSETOR" e valores em branco.
        """
        # Selecionar os dados da coluna B (ignora as primeiras 8 linhas)
        selected_data = data.iloc[8:509, 1]  # Índices baseados em zero (coluna B -> índice 1)
        records = []

        # Processar os dados
        for row in selected_data:
            if pd.isna(row) or "SUBSETOR" in str(row):  # Ignorar valores nulos ou "SUBSETOR"
                continue
            records.append({"Descritivo": row.strip()})  # Adiciona o valor formatado

        return records        
    
    def extrair_segmentos(self, data: pd.DataFrame):
        """
        Filtra os dados da coluna C, desconsiderando células com "SEGMENTO"
        e linhas onde a coluna D não está vazia.
        """
        # Seleção de linhas e colunas apropriadas
        selected_data = data.iloc[7:520, [2, 3]]  # Linhas 8 a 520, colunas C (índice 2) e D (índice 3)
        records = []

        try:
            for index, row in selected_data.iterrows():
                # Capturar os valores das colunas
                coluna_c = row[2]  # Coluna C
                coluna_d = row[3]  # Coluna D
                # Verificar condições para excluir a linha
                if pd.isna(coluna_c):                    
                    continue

                if str(coluna_c).strip() == "SEGMENTO":                    
                    continue

                if not pd.isna(coluna_d):                    
                    continue

                # Adicionar registros válidos
                records.append({"Descritivo": str(coluna_c).strip()})     

            # Remover duplicados do records usando um conjunto (set)
            unique_records = list({record["Descritivo"]: record for record in records}.values())

        except Exception as e:
            print(f"Erro ao processar os dados na linha {index}: {e}")

        return unique_records 
    
    def extrair_dados_empresa(self, data: pd.DataFrame):
        """
        Processa os dados do Excel e prepara para inserção na tabela Empresa.
        """
        records = []
        try:
            for index, row in data.iloc[7:520].iterrows():  # Linhas 8 a 520
                # Captura os valores das colunas
                setor_economico = row[0]  # Coluna A
                subsetor = row[1]  # Coluna B
                segmento_nome = row[2]  # Coluna C
                codigo = row[3]  # Coluna D
                segmento_classificacao_sigla = row[4]  # Coluna E

                # Ignorar linhas inválidas
                if pd.isna(segmento_nome) or str(segmento_nome).strip() == "SEGMENTO":
                    continue
                if pd.isna(codigo):  # Deve ter conteúdo na coluna D
                    continue
                
                # # Obter os IDs relacionados
                setor_economico_id = self.repositorio_segmento.obter_id(
                    "SetorEconomico", "Descritivo", 
                    self.encontrar_valor_acima(data, index, 0, "SETOR ECONÔMICO")
                )
                subsetor_id = self.repositorio_segmento.obter_id(
                    "Subsetor", "Descritivo", 
                    self.encontrar_valor_acima(data, index, 1, "SUBSETOR")
                )
                segmento_id = self.repositorio_segmento.obter_id(
                    "Segmento", "Descritivo", 
                    self.encontrar_valor_acima_segmento(data, index, 2, "SEGMENTO", 3)
                )
                segmento_classificacao_id = None
                if not pd.isna(segmento_classificacao_sigla):
                    segmento_classificacao_id = self.repositorio_segmento.obter_id(
                        "SegmentoClassificacao", "Sigla", segmento_classificacao_sigla
                    )

                # Adicionar registro válido
                records.append({
                    "Nome": str(segmento_nome).strip(),
                    "Codigo": str(codigo).strip(),
                    "SegmentoClassificacaoID": segmento_classificacao_id,
                    "SetorEconomicoID": setor_economico_id,
                    "SubsetorID": subsetor_id,
                    "SegmentoID": segmento_id
                })

        except Exception as e:
            print(f"Erro ao processar os dados: {e}")
        
        return records
    
    def encontrar_valor_acima(self, data, start_index, coluna_index, ignorar):
        """
        Encontra o primeiro valor não nulo acima do índice fornecido
        que não seja igual ao valor ignorado.
        """
        for i in range(start_index, -1, -1):  # Iteração acima da linha atual
            valor = data.iloc[i, coluna_index]
            if pd.isna(valor) or str(valor).strip() == ignorar:
                continue
            return str(valor).strip()
        return None
    
    def encontrar_valor_acima_segmento(self, data, start_index, coluna_index, ignorar, coluna_condicao):
        """
        Encontra o primeiro valor não nulo acima do índice fornecido
        que não seja igual ao valor ignorado e tenha a condição de que outra coluna
        (coluna_condicao) seja nula.
        
        :param data: DataFrame a ser processado.
        :param start_index: Índice inicial para iniciar a busca.
        :param coluna_index: Índice da coluna onde buscar o valor.
        :param ignorar: Valor a ser ignorado (exemplo: "SEGMENTO").
        :param coluna_condicao: Índice da coluna condicional que deve ser nula.
        """
        for i in range(start_index - 1, -1, -1):  # Iteração acima da linha atual
            valor = data.iloc[i, coluna_index]
            condicao = data.iloc[i, coluna_condicao]

            # Verificar se o valor é nulo, igual ao valor ignorado ou a coluna condicional não é nula
            if pd.isna(valor) or str(valor).strip() == ignorar or not pd.isna(condicao):
                continue

            # Retornar o valor válido
            return str(valor).strip()

        # Retorna None se nenhum valor válido for encontrado
        return None

