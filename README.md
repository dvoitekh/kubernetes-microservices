# Microservices in kubernetes
Simple Kubernetes-based app that contains 3 services:
1. Flask (Python) microservice (management of applications' logs)
2. Sinatra (Ruby) microservice (OAuth server - user registration and login)
3. MongoDB

The purpose of this app is to log history about web apps requests.

## Usage flow

By accessing Sinatra microservice:

1. Create user via `POST /users` endpoint by providing `username` and `password` as JSON
2. Login via `POST /login` endpoint by providing the same credentials (jwt token)

After that you can use Flask microservice (Warning! JWT authentication required). Flask microservice will query Sinatra auth microservice to check validity of token and resolve ID of the user via `GET /check_login` endpoint:

1. Take valid jwt token from previous step
2. Create application via `POST /applications` by providing `name` for the app as JSON
3. Check list of your current apps via `GET /applications`
4. Create log for particular app via `POST /logs/<application_id>` by providing `ip_address` and `request` (nested json) as JSON
5. Check list of the logs for this application `GET /logs/<application_id>`
6. See [flask app routes](https://github.com/dvoitekh/kubernetes-microservices/blob/master/flask-app/app/views.py) for some more routes

## Features

1. Containerized microservices ([flask](https://github.com/dvoitekh/kubernetes-microservices/tree/master/flask-app), [sinatra](https://github.com/dvoitekh/kubernetes-microservices/tree/master/sinatra-app))
2. Deployed to Kubernetes cluster (see [folder with kubernetes components](https://github.com/dvoitekh/kubernetes-microservices/tree/master/kubernetes))
3. Communication between microservices to resolve user's authentication
4. MongoDB storage
5. JWT authentication
6. Nginx proxy-server via [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/). See [its config for the project](https://github.com/dvoitekh/kubernetes-microservices/blob/master/kubernetes/ingress.yml)

## How to run

1. To run in development follow instructions on how to build related docker images written in [flask folder](https://github.com/dvoitekh/kubernetes-microservices/tree/master/flask-app) and [sinatra folder](https://github.com/dvoitekh/kubernetes-microservices/tree/master/sinatra-app))
2. In production follow [Kubernetes official guide](https://kubernetes.io/docs/tutorials/stateless-application/hello-minikube/) to deploy a cluster. Deploy all Kubernetes components from [Kubernetes config folder](https://github.com/dvoitekh/kubernetes-microservices/tree/master/kubernetes) for example via `kubectl apply -f <file>.yml`
