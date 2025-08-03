import requests
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")

def get_signatures(address,before=None,limit=1000):
    params = [address,{"limit": limit}]
    if before:
        params[1]["before"] = before
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": params
    }
    response = requests.post(RPC_URL, json=payload)
    return response.json().get("result", [])

def get_transaction(signature, encoding="jsonParsed", timeout=10):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"encoding": encoding, "commitment": "confirmed", "maxSupportedTransactionVersion": 0}]
    }
    response = requests.post(RPC_URL, json=payload, timeout=timeout)

    print(response)

    if response.json().get("result") is None:
        print("Transaction does not exist: ", response.json())
    
    return response.json().get("result", {})

