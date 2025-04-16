import pandas as pd
from domain.repositories.i_bovespa_repository import IBovespaRepository

class ProcessExcelService:
        def __init__ (self, bovespa_repository: IBovespaRepository):
            self.bovespa_repository = bovespa_repository

        async def ler_arquivo_excel_segmento_classificacao(self, arquivo_excel):
            segmentos_classificacao = []
            df = pd.read_excel(arquivo_excel, skiprows=519, nrows=9, usecols=[0])
            for index, row in df.iterrows():
                valor = row[0]
                sigla = valor.split('(')[1].split(')')[0]
                descritivo = valor.split(')')[1].strip()                
                objeto = {"Sigla": sigla, "Descritivo": descritivo}
                segmentos_classificacao.append(objeto)
            return segmentos_classificacao
            
        async def ler_setor_economico(self, arquivo_excel):
            setor_economico = []
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo_excel, skiprows=8, nrows=512, usecols=[0], header=None)
            # Desconsiderar as células que estejam com o valor SETOR ECONÔMICO ou valores em branco
            df = df.dropna()
            df = df[df[0] != 'SETOR ECONÔMICO']
            for index, row in df.iterrows():
                 valor = row[0]
                 descritivo = valor.split(')')[0].strip()
                 objeto = {"Descritivo": descritivo}      
                 setor_economico.append(objeto)
            return setor_economico
        
        async def importar_sub_setor(self, arquivo_excel):
            sub_setor_economico = []
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo_excel, skiprows=8, nrows=512, usecols=[1], header=None)
            # Desconsiderar as células que estejam com o valor SUBSETOR ou valores em branco
            df = df.dropna()
            df = df[df[1] != 'SUBSETOR']
            for index, row in df.iterrows():
                 valor = row[1]
                 descritivo = valor.split(')')[0].strip()
                 objeto = {"Descritivo": descritivo}      
                 sub_setor_economico.append(objeto)
            return sub_setor_economico
        
        async def importar_segmento(self, arquivo_excel):
            segmentos = []
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo_excel, skiprows=7, nrows=512, usecols=[2, 3], header=None)
            # Desconsiderar as células que estejam com o valor SEGMENTO na coluna C e que tenham conteúdo na coluna D
            df = df[(df[2] != 'SEGMENTO') & df[3].isna()]
            for index, row in df.iterrows():
                valor = row[2]
                if pd.isna(valor) or valor == 'SEGMENTO':  # você também pode verificar se o valor é 'SEGMENTO'
                    continue
                descritivo = valor.split(')')[0].strip()                
                objeto = {"Descritivo": descritivo}      
                segmentos.append(objeto)
            return segmentos
        
        async def importar_empresas(self, arquivo_excel):
            # Carregar os dados da planilha Excel
            df = pd.read_excel(arquivo_excel, skiprows=7, nrows=512, usecols=[0, 1, 2, 3, 4], header=None)
            # Criar uma lista para armazenar os dados
            dados = []
            # Iterar sobre as linhas do DataFrame
            for index, row in df.iterrows():
                # Verificar se a linha contém dados válidos
                if pd.notna(row[2]) and row[2] != 'SEGMENTO' and pd.notna(row[3]):
                    # Buscar os IDs das tabelas relacionadas
                    segmento_classificacao_id = None
                    if pd.notna(row[4]):
                        segmento_classificacao_id = self.bovespa_repository.buscar_segmento_classificacao_id(row[4])

                    setor_economico_id = self.bovespa_repository.buscar_setor_economico_id(self.buscar_valor_acima(df, 0, index, 'SETOR ECONÔMICO'))
                    subsetor_id = self.bovespa_repository.buscar_subsetor_id(self.buscar_valor_acima(df, 1, index, 'SUBSETOR'))

                    # Buscar o ID do segmento
                    segmento_descritivo = None
                    for i in range(index - 1, -1, -1):
                        valor = df[2].iloc[i]
                        if pd.notna(valor) and valor != 'SEGMENTO' and pd.isna(df[3].iloc[i]):
                            segmento_descritivo = valor
                            break
                    segmento_id = self.bovespa_repository.buscar_segmento_id(segmento_descritivo)

                    # Criar um dicionário com os dados
                    dados.append({
                        'Nome': row[2],
                        'Codigo': row[3],
                        'SegmentoClassificacaoID': segmento_classificacao_id,
                        'SetorEconomicoID': setor_economico_id,
                        'SubsetorID': subsetor_id,
                        'SegmentoID': segmento_id
                    })
            return dados
             
        # Função para buscar o valor da célula acima
        def buscar_valor_acima(self, df, coluna, linha, valor_ignorar):
            for i in range(linha - 1, -1, -1):
                valor = df[coluna].iloc[i]
                if pd.notna(valor) and valor != valor_ignorar:
                    return valor
            return None