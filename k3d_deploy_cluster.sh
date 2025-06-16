k3d cluster create sample-cluster

kubectl create namespace sample-app

# Server TLS configuration
kubectl -n sample-app create secret generic flask-server-tls \
  --from-file=server.crt=./tls/server.crt \
  --from-file=server.key=./tls/server.key \
  --from-file=ca.crt=./tls/ca.crt

# Client TLS configuration
kubectl -n sample-app create secret generic flask-client-tls \
  --from-file=client.crt=./tls/client.crt \
  --from-file=client.key=./tls/client.key \
  --from-file=ca.crt=./tls/ca.crt

kubectl -n sample-app apply -f k8s/server-service.yaml
kubectl -n sample-app apply -f k8s/server-deployment.yaml
kubectl -n sample-app apply -f k8s/client-deployment.yaml

kubectl create namespace monitoring

# Prometheus installation
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

# Chaos Mesh installation (using k3s container runtime)
helm repo add chaos-mesh https://charts.chaos-mesh.org
kubectl create ns chaos-mesh
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-mesh --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/k3s/containerd/containerd.sock --version 2.7.2
kubectl apply -f chaos-mesh/rbac.yaml

# ServiceMonitor whose purpose is to monitor the server service
kubectl apply -f k8s/flask-servicemonitor.yaml

# ConfigMap whose purpose is to make it possible to import the dashboard automatically
kubectl create configmap sample-dashboard --from-file=dashboards/ --namespace monitoring
kubectl label configmap sample-dashboard grafana_dashboard=1 --namespace monitoring