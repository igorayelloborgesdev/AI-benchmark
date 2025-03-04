docker stop chatgpt
docker rm chatgpt
docker build -t chatgpt-app .
docker run --name chatgpt --link sqlserver:sqlserver -p 8000:8000 -d chatgpt-app