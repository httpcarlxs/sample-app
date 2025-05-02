import requests
import time

def get_hello():
    while True:
        try:
            response = requests.get("http://flask-server:5000/")
            print(response.text)
        except requests.exceptions.RequestException as e:
            print("Error connecting to the server:", e)

        time.sleep(1)

if __name__ == "__main__":
    get_hello()
