# Imagem base para Python
FROM python:3.9-slim

# Definir a pasta de trabalho
WORKDIR /app

# Copiar os requisitos para a pasta de trabalho
COPY requirements.txt .

# Instalar os requisitos
RUN pip install -r requirements.txt
RUN pip install pymssql

# Copiar o código do aplicativo para a pasta de trabalho
COPY . .

# Expor a porta para o servidor
EXPOSE 8000

# Definir a comando para executar o aplicativo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]