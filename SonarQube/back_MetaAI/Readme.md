docker stop metaai
docker rm metaai
docker build -t metaai-app .
docker run --name metaai --link sqlserver:sqlserver -p 8004:8004 -d metaai-app
<!-- docker-compose -f docker-compose.debug.yml up -->
docker network create minha-rede
docker network connect back_metaai_metaai_network sqlserver
docker network connect back_metaai_metaai_network back_metaai-fastapi-app-1
docker exec -it back_metaai-fastapi-app-1 ping sqlserver