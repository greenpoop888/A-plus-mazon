import subprocess
import time
import requests
import os
import json

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
        print(f"Error: Unable to retrieve API information.\n{e}")
        exit(1)

def call_api(method, url, headers, json_data=None):
    try:
        if method == "GET":
            res = requests.get(url, headers=headers, json=json_data)
        elif method == "POST":
            res = requests.post(url, headers=headers, json=json_data)
        else:
            return None

        print(f"{method} {url}: {json_data} -> {res.status_code}")
        return res
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def query_quantity(base_url, api_key, min_stock=10):
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    print(f"Querying inventory...")
    return call_api("GET", f"{base_url}/inventory_need_restock?min_stock={min_stock}", headers)

def add_quantity(base_url, api_key, to_restock_inventory, restock_amount):
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    
    payload = [{**item, "add_amount": restock_amount} for item in to_restock_inventory]

    print(f"Adding quantity (+{restock_amount})...")
    call_api("POST", f"{base_url}/add", headers, json_data=payload)

if __name__ == "__main__":
    print("Starting restock generator...")
    
    while True:
        try:
            min_stock = int(input("Enter minimum stock level to trigger restock (e.g., 10): "))
            if min_stock < 1:
                print("Error: Minimum stock level must be at least 1.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    while True:
        try:
            restock_amount = int(input("Enter the amount to add for each restock (e.g., 2000): "))
            if restock_amount < 1:
                print("Error: Restock amount must be at least 1.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    apigateway_url, api_key = get_api_info()
    interval = 1.0
    
    try:
        while True:
            response = query_quantity(apigateway_url, api_key, min_stock)
            
            if response and response.status_code == 200:
                to_restock_inventory = response.json() 
                
                if to_restock_inventory:
                    add_quantity(apigateway_url, api_key, to_restock_inventory, restock_amount)
                else:
                    print("Inventory is healthy, no restock needed.")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")