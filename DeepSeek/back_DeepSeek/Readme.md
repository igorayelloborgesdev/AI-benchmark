docker stop deepseek
docker rm deepseek
docker build -t deepseek-app .
docker run --name deepseek --link sqlserver:sqlserver -p 8002:8002 -d deepseek-app