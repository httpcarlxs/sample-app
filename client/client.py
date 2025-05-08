import requests, json, time
from datetime import datetime

def get_hello():
    while True:
        try:
            response = requests.get("http://flask-server:5000/")
            now = datetime.now().strftime("%H:%M:%S")
            msg = response.json()['message']
            #print(json.dumps(response.json(), indent=4))
            print(now, '|', msg)
        except requests.exceptions.RequestException as e:
            print("Error connecting to the server:", e)

        time.sleep(5)

if __name__ == "__main__":
    get_hello()
