from rpc_utils import get_signatures, get_transaction
import time
import json
import os
import requests


def load_last_signature(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        lines = f.readlines()
        return json.loads(lines[-1]) if lines else None

def append_signatures_and_transactions(address: str, name: str, delay: float = .02, limit=1000, retries=10):
    sig_path = f"./data/txs/{address}/{name}_signatures.jsonl"
    tx_path = f"./data/txs/{address}/{name}_transactions.jsonl"

    os.makedirs(os.path.dirname(sig_path), exist_ok=True)
    os.makedirs(os.path.dirname(tx_path), exist_ok=True)

    before_sig = load_last_signature(sig_path)
    before = before_sig if isinstance(before_sig, str) else None

    while True:
        new_sigs = get_signatures(address, before=before, limit=limit)

        if not new_sigs:
            print(f"No new signatures found for {name}.")
            return

        with open(sig_path, "a") as sig_file, open(tx_path, "a") as tx_file:
            for sig_entry in new_sigs:
                signature = sig_entry["signature"]
                json.dump(signature, sig_file)
                sig_file.write("\n")

                for _ in range(retries):
                    try:
                        print(f"Fetching transaction for signature: {signature}")
                        tx_data = get_transaction(signature)
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"Request error on signature {signature}, retrying {_+1}/10: {e}")
                        time.sleep(1)
                else:
                    print(f"Failed to fetch transaction {signature} after {retries} retries.")
                    return

                json.dump(tx_data, tx_file)
                tx_file.write("\n")


                time.sleep(delay)
            before = new_sigs[-1]["signature"]

def main():
    global POOL_ADDRESS
    POOL_ADDRESS = "HTvjzsfX3yU6BUodCjZ5vZkUrAxMDTrBs3CJaq43ashR"
    name = "sol_usdc"

    print(f"Fetching data for {name}:{POOL_ADDRESS}")
    append_signatures_and_transactions(POOL_ADDRESS, name, delay=.019)

if __name__ == "__main__":
    main()