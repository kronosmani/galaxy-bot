import requests

api_key = "c3bc52f3a84cf4a861fd3f9787c1ef3c"
url = f"https://galaxyonline.io/api/galaxy-users/get-warnings?key={api_key}"

# Указываем прокси как None, чтобы обойти блокировку
proxies = {
    "http": None,
    "https": None,
}

response = requests.get(url, proxies=proxies)

if response.status_code == 200:
    print("API Response:", response.json())
else:
    print(f"API Error: {response.status_code}")