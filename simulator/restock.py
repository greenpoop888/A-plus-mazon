import subprocess
import time
import requests
import os

API_KEY_NAME = "ClientApiKey" 

def get_api_info():
    try:
        print("retreiving api info...")
        infra_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "infra"))

        api_url = subprocess.check_output(
            ["terraform", "output", "-raw", "api_base_url"], 
            cwd=infra_dir, 
            shell=True
        ).decode("utf-8").strip()
        
        key_id = subprocess.check_output([
            "aws", "apigateway", "get-api-keys", 
            "--name-query", API_KEY_NAME, 
            "--query", "items[0].id", 
            "--output", "text"
        ], shell=True).decode("utf-8").strip()
        
        api_key = subprocess.check_output([
            "aws", "apigateway", "get-api-key", 
            "--api-key", key_id, 
            "--include-value", 
            "--query", "value", 
            "--output", "text"
        ], shell=True).decode("utf-8").strip()
        
        return api_url, api_key
    except Exception as e:
        print(f"Error: Unable to retrieve API information. Please ensure terraform apply has been successful and AWS CLI is configured.\n{e}")
        exit(1)

def call_api(method, url, headers, json_data=None):
    try:
        if method == "GET":
            res = requests.get(url, headers=headers, json=json_data)
        elif method == "POST":
            res = requests.post(url, headers=headers, json=json_data)
        else:
            print(f"Unsupported method: {method}")
            return None

        print(f"{method} {url}: {json_data} -> {res.status_code}")
        print(f"Response: {res.text}")
        return res
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def query_quantity(base_url, api_key):
    if not base_url: return

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    print(f"Querying inventory...")
    call_api("GET", f"{base_url}/inventory_need_restock", headers)

def add_quantity(base_url, api_key, to_restock_inventory):
    if not base_url: return

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = [{**item, "add_amount": 2000} for item in to_restock_inventory]

    print(f"Adding quantity...")
    call_api("POST", f"{base_url}/add", headers, json_data=payload)

if __name__ == "__main__":
    print("Starting restock generator...")

    apigateway_url, api_key = get_api_info()
    interval = 1.0
    
    try:
        while True:
            to_restock_inventory = query_quantity(f"{apigateway_url}", api_key)
            if to_restock_inventory :
                add_quantity(f"{apigateway_url}", api_key, to_restock_inventory)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")
                