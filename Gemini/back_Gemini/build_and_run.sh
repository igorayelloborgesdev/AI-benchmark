#!/bin/bash

# Parar e remover o container existente
docker stop gemini
docker rm gemini

# Construir a imagem
docker build -t gemini-app .

# Executar o container
docker run --name gemini --link sqlserver:sqlserver -p 8003:8003 -d gemini-app