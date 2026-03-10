import subprocess
import time
import requests
import os
import random

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

def call_api(url, headers, json_data=None):
    try:
        res = requests.post(url, headers=headers, json=json_data)
        
        print(f"Post {url}: {json_data} -> {res.status_code}")
        print(f"Response: {res.text}")
        return res
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def generate_request(base_url, api_key, min_purchase = 1, max_purchase = 10):
    if not base_url: return

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    sid = random.randint(1, 2) 
    pid = random.randint(1, 9)
    quantity = random.randint(min_purchase, max_purchase)

    print(f"Deduct {quantity} of product_id = {pid} from store_id = {sid}")
    call_api(f"{base_url}/deduct", headers, json_data={"store_id": sid, "product_id": pid, "quantity": quantity})


if __name__ == "__main__":
    print("Starting traffic generator...")
    while True:
        try:
            input_rate = int(input("How many requests per second? (e.g., 1): "))
            if input_rate < 1:
                print("Error: Minimum input rate must be at least 1.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")
    
    while True:
        try:
            min_purchase = int(input("Enter minimum purchase quantity (e.g., 1): "))
            if min_purchase < 1:
                print("Error: Minimum purchase must be at least 1.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    while True:
        try:
            max_purchase = int(input("Enter maximum purchase quantity (e.g., 10): "))
            if max_purchase < min_purchase:
                print(f"Error: Maximum purchase cannot be less than minimum ({min_purchase}).")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    base_url, api_key = get_api_info()
    try:
        rate = float(input_rate)
        if rate <= 0:
            print("Please enter a number greater than 0.")
        else:
            interval = 1.0 / rate
            print(f"Target rate: {rate} req/s")
            
            while True:
                generate_request(f"{base_url}", api_key, min_purchase, max_purchase)
                time.sleep(interval)
                
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
    except KeyboardInterrupt:
        print("\nStopped by user.")