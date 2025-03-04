docker stop metaai
docker rm metaai
docker build -t metaai-app .
docker run --name metaai --link sqlserver:sqlserver -p 8004:8004 -d metaai-app