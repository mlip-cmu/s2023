# Recitation 10: Container Orchestration with Kubernetes


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
    - Install Helm:
        ```
        sudo snap install helm --classic
        ```
    - Add the prometheus-community Helm repository:
        ```
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        ```

## Demo
1. Build a docker image from the docker file in `server/` :
    ```
    docker build -t server:flask server
    ```
2. Create a Kind Cluster with the following command:
    ```
    kind create cluster --config configs/kind-config.yaml
    ```
    This will create a cluster with 3 nodes. You can see the nodes by running:
    ```
    kubectl get nodes
    ```
3. Load the docker image into the cluster:
    ```
    kind load docker-image server:flask
    ```
4. Deploy the server to the cluster:
    ```
    kubectl apply -f configs/cluster-config.yaml
    ```
    - To view all running pods, services, etc., run:
        ```
        kubectl get all -o wide
        ```
    - To view the logs of a pod, run:
        ```
        kubectl logs <pod-name> [-f]
        ```
5. Let us now query some end points on the Flask server via the NodePort Service
    - To get the NodePort Service IP:
        ```
        kubectl get svc -o wide
        ```
    - To get the Control Node IP:
        ```
        kubectl get nodes -o wide
        ```
    - To query the server:
        ```
        curl http://<Control-Node-IP>:<NodePort-Port>/
        ```
    - To kill the server:
        ```
        curl http://<Control-Node-IP>:<NodePort-Port>/health/kill
        ```
        Once the server is Killed, you can see that the pod is restarted by running:
        ```
        kubectl get pods -o wide
        ```
        
    - Some other endpoints:
        ```
        # End point to see server status
        curl http://<Control-Node-IP>:<NodePort-Port>/health/status

        # End point to get the current time
        curl http://<Control-Node-IP>:<NodePort-Port>/datetime
        ```
6. To setup Prometheus and Grafana with Helm:
    ```
    # Replace [RELEASE_NAME] with a name of your choice
    helm install [RELEASE_NAME] prometheus-community/kube-prometheus-stack

    ```
7. To be able to view the Prometheus and Grafana UI, we need to forward the ports:
    - For Prometheus:
        ```
        kubectl port-forward --address 0.0.0.0 service/prom-kube-prometheus-stack-prometheus  9090
        ```
    - For Grafana:
        ```
        kubectl port-forward --address 0.0.0.0 service/prom-grafana 3000:80
        ```
8. To view the UIs:
    - For Prometheus:
        - Open `http://<VM-IP>:9090`
    - For Grafana:
        - Open `http://<VM-IP>:3000`
        - Username: `admin`, Password: `prom-operator`

## Cleanup
The entire cluster can be deleted by running:
```
kind delete cluster
```

However, for individual components of our deployment, we can run the following commands:
- To delete the server deployment along with the NodePort service:
    ```
    kubectl delete -f configs/cluster-config.yaml
    ```
- To bring down the Prometheus and Grafana Helm release:
    ```
    helm uninstall [RELEASE_NAME]
    ```
- To delete the Docker Image we built earlier:
    ```
    docker rmi server:flask
    ```


## Additional Commands
- Docker
    ```
    # To run the docker image locally
    docker run -p 5555:5555 server:flask

    # To enter one of the nodes in the cluster
    docker exec -it <node-name> sh
    ```

- Kubernetes
    ```
    # To port forward our server to the host machine
    kubectl port-forward svc/server-service 5555:5555

    # To get the password for the Grafana UI
    kubectl get secret --namespace default prom-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

    # To get information about a specific resource
    kubectl describe <resource-type> <resource-name>

    ```
- Helm
    ```
    # To search for a Helm chart from the prometheus-community repository
    helm search repo prometheus-community

    # To list all Helm releases
    helm list
    ```



## Resources
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kind Documentation](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Helm Documentation](https://helm.sh/docs/intro/quickstart/)
