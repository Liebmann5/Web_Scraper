import requests
import json
import time

# Oxylabs credentials
username = "{customers-USERNAME}"
password = "{customers-PASSWORD}"

# Oxylabs endpoints
proxies_endpoint = "https://api.oxylabs.io/v1/proxies"
captcha_endpoint = "https://api.oxylabs.io/v1/captcha/solve"

# Target URL and CAPTCHA image URL
target_url = "https://example.com"
captcha_image_url = "https://example.com/captcha.jpg"

# Other parameters for CAPTCHA solving
other_params = {
    "param1": "value1",
    "param2": "value2"
}

# Function to get a list of proxies
def get_proxies():
    response = requests.get(proxies_endpoint, auth=(username, password))
    return json.loads(response.text)

# Function to rotate IP address
def rotate_ip(proxies):
    for proxy in proxies:
        proxy_endpoint = f"http://{proxy['ip']}:{proxy['port']}"
        proxies_config = {
            "http": proxy_endpoint,
            "https": proxy_endpoint
        }
        try:
            response = requests.get(target_url, proxies=proxies_config)
            print(f"Response status code: {response.status_code}")
            
            # Check the assigned IP address
            ip_check_response = requests.get('https://ip.oxylabs.io', proxies=proxies_config)
            print(f"Assigned IP: {ip_check_response.text}")
            
        except Exception as e:
            print(f"Failed to send request with proxy {proxy_endpoint}: {e}")

        # Wait for a while before rotating to the next IP
        time.sleep(5)

# Function to solve CAPTCHA
def solve_captcha():
    response = requests.post(captcha_endpoint, auth=(username, password), json={
        "captcha_url": captcha_image_url,
        "other_params": other_params
    })
    solution = json.loads(response.text)["solution"]
    print(f"Captcha solution: {solution}")

# Function to run the IP rotation and CAPTCHA solving
def run_oxylabs_tasks():
    # Get a list of proxies
    proxies = get_proxies()

    # Rotate IP addresses
    rotate_ip(proxies)

    # Solve CAPTCHA
    solve_captcha()


# Call the function to run the tasks
run_oxylabs_tasks()