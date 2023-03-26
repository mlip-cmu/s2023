# Recitation 10: Container Orchestration with Kubernetes
---

## Overview
In this recitation, we explore Kubernetes, a container orchestration system. We will use Kind to deploy a local Kubernetes cluster. While this recitation aims to introduce you to Kubernetes, it is not meant to be a comprehensive guide. For more information, please refer to the [Kubernetes documentation](https://kubernetes.io/docs/home/).

*Note: Kind is not a production ready system and is used in this recitation only to demo a subset of capabilities of Kubernetes*


## Installation
- *Docker* - Docker is installed by default on most Linux distributions. However, if you do not have it, you can install it by following the instructions [here](https://docs.docker.com/engine/install/).
- *Kind* - Kind is a tool for running local Kubernetes clusters using Docker container “nodes”. You can install it with the following on Linux:
    ```
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
    ```
- *kubectl* - kubectl is a command-line tool for controlling Kubernetes clusters. You can install it with the following on Linux:
    ```
    sudo snap install kubectl --classic
    ```
- *Helm* - Helm is a package manager for Kubernetes. You can install it with the following on Linux:
    ```
    sudo snap install helm --classic
    ```

---
# TODO
## Commands
```
kind create cluster --config configs/kind-config.yaml
docker build -t server:flask .
docker run -p 5555:5555 server:flask
kubectl apply -f configs/cluster-config.yaml
kind load docker-image server:flask
kubectl get all -o wide
kubectl port-forward svc/server-service 5555:5555
kubectl get secret --namespace default prom-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
snap install kubectl --classic
sudo snap install helm --classic
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm search repo prometheus-community
helm install [RELEASE_NAME] prometheus-community/kube-prometheus-stack
helm uninstall [RELEASE_NAME]
kubectl port-forward --address 0.0.0.0 service/prom-grafana 3000:80
kubectl port-forward --address 0.0.0.0 service/prom-kube-prometheus-stack-prometheus  9090

```

## Ordering
```
docker build -t server:flask .
kind create cluster --config configs/kind-config.yaml
kind load docker-image server:flask
kubectl apply -f configs/cluster-config.yaml
kubectl port-forward --address 0.0.0.0 service/prom-grafana 3000:80
kubectl port-forward --address 0.0.0.0 service/prom-kube-prometheus-stack-prometheus  9090
```

## Resources
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kind Documentation](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Helm Documentation](https://helm.sh/docs/intro/quickstart/)
