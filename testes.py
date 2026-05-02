import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb2N0b3IiLCJleHAiOjE3NzgzNTE2ODJ9.agLRu-xfqKedi_Z_FjI_QHqJHKFJjYqNR_GFLFMmsaE"
}

request = requests.get("http://127.0.0.1:8000/doctor/refresh", headers=headers) 
print(request)
print(request.json())
