import requests

username = "customer-USER"
password = "PASS"
proxy = "pr.oxylabs.io:7777"

proxies = {
    'http': f'http://{username}:{password}@{proxy}',
    'https': f'http://{username}:{password}@{proxy}',
}

response = requests.request(
    'GET',
    'https://ip.oxylabs.io',
    proxies=proxies,
)

print(response.text)