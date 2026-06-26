import requests
try:
    r = requests.get("http://localhost:8000/api/politicians")
    print(r.status_code)
    print(r.text[:500])
except Exception as e:
    print(e)
