import requests

if __name__ == "__main__":
    response = requests.post("http://localhost:8081/")
    print(response.json())