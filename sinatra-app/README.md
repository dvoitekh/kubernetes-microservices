# Sinatra authentication microservice

## How to build and run container

1. `cp .env.example .env`
2. `docker build -t sinatra-auth .`
3. `docker run --env-file .env -p 5001:5001 sinatra-auth:latest`
