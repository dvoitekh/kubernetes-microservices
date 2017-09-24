# flask-logger
Simple Flask web app that logs data about other applications requests.

## Features

1. Containerized application
2. App is deployed to Kubernetes cluster (see [folder with kubernetes components](https://github.com/dvoitekh/flask-logger/tree/master/kubernetes))
3. MongoDB storage
4. JWT authentication

## How to run

1. In development simply run `python run.py` (ensure you have MongoDB up and running in container)
2. In production follow [Kubernetes official guide](https://kubernetes.io/docs/tutorials/stateless-application/hello-minikube/) to deploy a cluster
