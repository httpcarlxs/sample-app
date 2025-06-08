# server/server.py

from flask import Flask, jsonify, request, abort
from datetime import datetime
import ssl, os, time
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# 1) Define your “hello world” route
@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Secure Hello World!"
    return jsonify(message=msg)

# 2) Create Prometheus metrics and attach hooks
server_requests = Counter(
    "server_requests_total",
    "Total amount of requests received by the server",
)

SHARED_KEY = os.getenv("PROMETHEUS_HEX")

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_metrics(response):
    # Don’t count favicon or the /metrics calls as “server_requests”:
    if request.path not in ['/favicon.ico', '/metrics']:
        server_requests.inc()
    return response

# 3) Expose /metrics with Bearer-token authentication
@app.route("/metrics")
def metrics():
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        abort(401)
    token = auth_header.split(" ")[1]

    print(token)
    print(SHARED_KEY)

    if token != SHARED_KEY:
        abort(403)
    # Return all Prometheus metrics in text format:
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

# 4) Finally, start the app with mTLS
if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # server.crt/server.key signed by your CA:
    context.load_cert_chain(certfile="tls/server.crt", keyfile="tls/server.key")
    # Trust the same CA for client certs:
    context.load_verify_locations(cafile="tls/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED

    # Flask listens on 0.0.0.0:5000 over HTTPS
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
