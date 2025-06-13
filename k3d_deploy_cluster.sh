k3d cluster create sample-cluster

kubectl create namespace sample-app

# Configurações para TLS do servidor
kubectl -n sample-app create secret generic flask-server-tls \
  --from-file=server.crt=./tls/server.crt \
  --from-file=server.key=./tls/server.key \
  --from-file=ca.crt=./tls/ca.crt

# Configurações para TLS do cliente
kubectl -n sample-app create secret generic flask-client-tls \
  --from-file=client.crt=./tls/client.crt \
  --from-file=client.key=./tls/client.key \
  --from-file=ca.crt=./tls/ca.crt

kubectl -n sample-app apply -f k8s/server-service.yaml
kubectl -n sample-app apply -f k8s/server-deployment.yaml
kubectl -n sample-app apply -f k8s/client-deployment.yaml

kubectl create namespace monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

# ServiceMonitor que serve para monitorar o service do servidor
kubectl apply -f k8s/flask-servicemonitor.yaml

# ConfigMap que serve para importar automaticamente o dashboard Grafana
kubectl create configmap sample-dashboard --from-file=dashboards/ --namespace monitoring
kubectl label configmap sample-dashboard grafana_dashboard=1 --namespace monitoring