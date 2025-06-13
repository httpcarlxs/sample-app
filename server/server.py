from flask import Flask, jsonify, request
from datetime import datetime
import ssl
from prometheus_client import Counter, generate_latest

app = Flask(__name__)


@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Secure Hello World!"
    return jsonify(message=msg)


# Prometheus counter metric that counts the amount of requests received by the flask-server. 
# It is possible to query this metric by inputting "flask_server_requests_total" in the Prometheus query text field.
server_requests = Counter(
    "flask_server_requests_total",
    "Total amount of requests received by the server",
)


@app.after_request
def track_metrics(response):
    """_summary_
        After each request, update the Prometheus metrics.

    Args:
        response: The response from the main request made.

    Returns:
        The response from the main request made.
    """
    if request.path != "/metrics":
        server_requests.inc()
    return response


@app.route("/metrics")
def metrics():
    """_summary_
        Return the latest Prometheus metrics. The metrics are scraped periodically by Prometheus.

    Returns:
        The latest Prometheus metrics.
    """
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="tls/server.crt", keyfile="tls/server.key")
    context.load_verify_locations(cafile="tls/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
