import subprocess
import requests
import json
import time
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

def call_api(method, url, headers, params=None, json_data=None):
    try:
        if method == "GET":
            res = requests.get(url, headers=headers, params=params)
        else:
            res = requests.post(url, headers=headers, json=json_data)
        
        print(f"{method} {url}: {params if params else json_data} -> {res.status_code}")
        print(f"Response: {res.text}")
        return res
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    base_url, api_key = get_api_info()
    if not base_url: return

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # ---------------------------------------------------------
    # 1. GET /inventory & /price (test ID 1 & 2)
    # ---------------------------------------------------------
    print(f"\n{'='*30}\n[TEST] Inventory & Price (ID 1, 2)\n{'='*30}")
    for pid in ["1", "2"]:
        # Inventory
        call_api("GET", f"{base_url}/inventory", headers, 
                 params={"store_id": "1", "product_id": pid, "min_amount": 30})
        # Price
        call_api("GET", f"{base_url}/price", headers, 
                 params={"store_id": "1", "product_id": pid})

    # ---------------------------------------------------------
    # 2. POST /deduct (test ID 1 & 2)
    # ---------------------------------------------------------
    print(f"\n{'='*30}\n[TEST] Deduct Single (ID 1, 2)\n{'='*30}")
    for pid in ["1", "2"]:
        call_api("POST", f"{base_url}/deduct", headers, 
                 json_data={"store_id": "1", "product_id": pid, "quantity": 1})

    # ---------------------------------------------------------
    # 3. POST /deduct-batch 
    # ---------------------------------------------------------
    print(f"\n{'='*30}\n[TEST] Deduct Batch\n{'='*30}")
    
    # First batch: ID 1 & 2 (should return 200)
    print("--- Batch 1 (Product 1 & 2) ---")
    batch1 = {
        "store_id": "1",
        "items": [
            {"product_id": "1", "quantity": 1},
            {"product_id": "2", "quantity": 1}
        ]
    }
    call_api("POST", f"{base_url}/deduct-batch", headers, json_data=batch1)

    # Second batch: ID 3 & 4 (should return 400 due to insufficient stock)
    print("\n--- Batch 2 (Product 3 & 4) ---")
    batch2 = {
        "store_id": "1",
        "items": [
            {"product_id": "3", "quantity": 1},
            {"product_id": "4", "quantity": 1}
        ]
    }
    call_api("POST", f"{base_url}/deduct-batch", headers, json_data=batch2)

    # ---------------------------------------------------------
    # 4. Error Handling
    # ---------------------------------------------------------
    print(f"\n{'='*30}\n[TEST] Error Handling Case\n{'='*30}")
    
    # Case A: Invalid store/product IDs (404)
    print("Case A: Invalid IDs (Expect 404)")
    call_api("GET", f"{base_url}/inventory", headers, 
             params={"store_id": "999", "product_id": "999", "min_amount": 1})

    # Case B: Insufficient stock (Expect 400)
    print("\nCase B: Insufficient Stock (Expect 400)")
    call_api("POST", f"{base_url}/deduct", headers, 
             json_data={"store_id": "1", "product_id": "1", "quantity": 999999})

    # Case C: Invalid route (Expect 404)
    print("\nCase C: Invalid Route (Expect 404)")
    call_api("GET", f"{base_url}/undefined_route", headers)

if __name__ == "__main__":
    main()