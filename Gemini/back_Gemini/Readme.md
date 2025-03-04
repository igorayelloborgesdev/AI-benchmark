docker stop gemini
docker rm gemini
docker build -t gemini-app .
docker run --name gemini --link sqlserver:sqlserver -p 8003:8003 -d gemini-app