from flask import Flask, jsonify
from datetime import datetime
import ssl

app = Flask(__name__)

@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Secure Hello World!"
    return jsonify(message=msg)


if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile="tls/server.crt", keyfile="tls/server.key")
    context.load_verify_locations(cafile="tls/ca.crt")
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
