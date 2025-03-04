docker stop fastapi
docker rm fastapi
docker build -t fastapi-app .
docker run --name fastapi --link sqlserver:sqlserver -p 80:80 -d fastapi-app