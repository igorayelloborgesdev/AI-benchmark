# Usar uma imagem oficial do Python
FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expor a porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar o FastAPI usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
