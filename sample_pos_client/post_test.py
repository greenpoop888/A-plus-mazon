import subprocess
import requests
import json
import time

API_KEY_NAME = "ClientApiKey" 

def get_api_info():
    try:
        print("retreiving api info...")
        api_url = subprocess.check_output(["terraform", "output", "-raw", "api_base_url"], shell=True).decode("utf-8").strip()
        
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

def run_test(name, func):
    """Test helper function, runs twice to meet assignment requirements"""
    print(f"\n{'='*20}\nTesting: {name}\n{'='*20}")
    for i in range(1, 3):
        print(f"Attempt #{i}:")
        func()
        time.sleep(1) 

def main():
    base_url, api_key = get_api_info()
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    sid = "1"
    pid = "101"

    # --- 1. GET /inventory ---
    def test_inventory():
        url = f"{base_url}/inventory"
        params = {"storeId": sid, "productId": pid, "minAmount": 1}
        res = requests.get(url, headers=headers, params=params)
        print(f"GET {url} -> {res.status_code}\n{res.text}")

    # --- 2. GET /price ---
    def test_price():
        url = f"{base_url}/price"
        params = {"storeId": sid, "productId": pid}
        res = requests.get(url, headers=headers, params=params)
        print(f"GET {url} -> {res.status_code}\n{res.text}")

    # --- 3. POST /deduct ---
    def test_deduct():
        url = f"{base_url}/deduct"
        data = {"storeId": sid, "productId": pid, "quantity": 1}
        res = requests.post(url, headers=headers, json=data)
        print(f"POST {url} -> {res.status_code}\n{res.text}")

    # --- 4. POST /deduct-batch ---
    def test_batch():
        url = f"{base_url}/deduct-batch"
        data = {
            "storeId": sid,
            "items": [
                {"id": pid, "qty": 1},
                {"id": "102", "qty": 1}
            ]
        }
        res = requests.post(url, headers=headers, json=data)
        print(f"POST {url} -> {res.status_code}\n{res.text}")

    run_test("Check Inventory", test_inventory)
    run_test("Check Price", test_price)
    run_test("Deduct Single Item", test_deduct)
    run_test("Deduct Batch Items", test_batch)

if __name__ == "__main__":
    main()