import requests
import time
from datetime import datetime

def get_hello():
    while True:
        try:
            response = requests.get("http://flask-server:5000/")
            now = datetime.now().strftime("%H:%M:%S")
            print(now, '|', response.text)
        except requests.exceptions.RequestException as e:
            print("Error connecting to the server:", e)

        time.sleep(5)

if __name__ == "__main__":
    get_hello()
