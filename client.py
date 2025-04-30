import requests

def get_hello():
    try:
        response = requests.get("http://localhost:5000/")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print("Error connecting to the server:", e)

if __name__ == "__main__":
    get_hello()
