```
docker build -t sinatra-auth .
docker run --env-file .env -p 5001:5001 sinatra-auth:latest
```
