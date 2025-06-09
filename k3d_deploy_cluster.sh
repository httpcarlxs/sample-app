mkdir -p ~/k3d-data/prometheus
mkdir -p ~/k3d-data/grafana

k3d registry create sample-registry.localhost --port 5001

k3d cluster create mycluster \
  --registry-use k3d-sample-registry.localhost:5001 \
  --agents 0 \
  --servers 1 \
  --volume ~/k3d-data/prometheus:/var/lib/rancher/k3s/storage/prometheus@server:0 \
  --volume ~/k3d-data/grafana:/var/lib/rancher/k3s/storage/grafana@server:0 \
  --k3s-arg "--disable=traefik@server:*"

docker build -f server/Dockerfile -t flask-server:mtls ./server
docker tag flask-server:mtls k3d-sample-registry.localhost:5001/flask-server:mtls
docker push k3d-sample-registry.localhost:5001/flask-server:mtls

docker build -f client/Dockerfile -t flask-client:mtls ./client
docker tag flask-client:mtls k3d-sample-registry.localhost:5001/flask-client:mtls
docker push k3d-sample-registry.localhost:5001/flask-client:mtls

k3d image import flask-server:mtls --cluster mycluster
k3d image import flask-client:mtls --cluster mycluster

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

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --values ../yaml/persistence.yaml

# export PROMETHEUS_HEX="6a39a8d315aded11a5e14f97336c037ff99a974463614edc149d87cf24b72bb4"

kubectl apply -f k8s/bearer-token-secret.yaml
kubectl apply -f k8s/flask-servicemonitor.yaml
