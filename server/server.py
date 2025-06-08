from flask import Flask, jsonify, request, abort
from datetime import datetime
import ssl, os, time
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Secure Hello World!"
    return jsonify(message=msg)

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
    if request.path not in ['/favicon.ico', '/metrics']:
        server_requests.inc()
    return response

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
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="tls/server.crt", keyfile="tls/server.key")
    context.load_verify_locations(cafile="tls/ca.crt")
    context.verify_mode = ssl.CERT_REQUIREDi
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
