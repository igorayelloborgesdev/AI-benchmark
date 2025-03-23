docker stop copilot
docker rm copilot
docker build --no-cache -t copilot-app .
docker run --name copilot --link sqlserver:sqlserver -p 8001:8001 -d copilot-app