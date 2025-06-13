k3d registry create sample-registry.localhost --port 5001

k3d cluster create sample-cluster \
  --registry-use k3d-sample-registry.localhost:5001 \
  --agents 0 \
  --servers 1

docker build -f server/Dockerfile -t flask-server:mtls ./server
docker tag flask-server:mtls k3d-sample-registry.localhost:5001/flask-server:mtls
docker push k3d-sample-registry.localhost:5001/flask-server:mtls

docker build -f client/Dockerfile -t flask-client:mtls ./client
docker tag flask-client:mtls k3d-sample-registry.localhost:5001/flask-client:mtls
docker push k3d-sample-registry.localhost:5001/flask-client:mtls

k3d image import flask-server:mtls --cluster sample-cluster
k3d image import flask-client:mtls --cluster sample-cluster

kubectl create namespace sample-app

kubectl -n sample-app create secret generic flask-server-tls \
  --from-file=server.crt=./tls/server.crt \
  --from-file=server.key=./tls/server.key \
  --from-file=ca.crt=./tls/ca.crt

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

kubectl apply -f k8s/flask-servicemonitor.yaml

kubectl create configmap sample-dashboard   --from-file=dashboards/   -n monitoring
kubectl label configmap sample-dashboard grafana_dashboard=1 -n monitoring