import requests

response = requests.get("https://fastapi-project-zt0d.onrender.com/users/stream", stream=True)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
