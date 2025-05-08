from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    now = datetime.now().strftime("%H:%M:%S")
    msg = now + " -- Hello, World!"
    return jsonify(message=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
