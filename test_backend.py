import requests
import json

url = "http://localhost:8000/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "How do I install eCOMET?"}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
