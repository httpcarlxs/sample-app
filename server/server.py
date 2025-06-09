from flask import Flask, jsonify, request, abort
from datetime import datetime
import ssl, os
from prometheus_client import Counter, generate_latest

app = Flask(__name__)


@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Secure Hello World!"
    return jsonify(message=msg)


server_requests = Counter(
    "flask_server_requests_total",
    "Total amount of requests received by the server",
)


@app.after_request
def track_metrics(response):
    if request.path not in ["/favicon.ico", "/metrics"]:
        server_requests.inc()
    return response


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="tls/server.crt", keyfile="tls/server.key")
    context.load_verify_locations(cafile="tls/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
