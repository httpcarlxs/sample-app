from flask import Flask, jsonify
from datetime import datetime
import ssl

app = Flask(__name__)

@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Hello, World com SSL!"
    return jsonify(message=msg)

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('tls/server-cert.crt', 'tls/server-key.key')
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
