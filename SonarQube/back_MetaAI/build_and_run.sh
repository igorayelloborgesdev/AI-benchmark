#!/bin/bash

# Parar e remover o container existente
docker stop metaai
docker rm metaai

# Construir a imagem
docker build -t metaai-app .

# Executar o container
docker run --name metaai --link sqlserver:sqlserver -p 8004:8004 -d metaai-app