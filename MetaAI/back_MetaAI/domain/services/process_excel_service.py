import pandas as pd

class ProcessExcelService:
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
            