import json
from web3 import Web3

# --- 1. CONNECT TO YOUR LOCAL GANACHE BLOCKCHAIN ---
# Ganache runs on this address by default
ganache_url = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if the connection is successful
if not web3.is_connected():
    print(" ERROR: Could not connect to Ganache.")
    print("Please make sure Ganache is running and you clicked 'Quickstart'.")
    exit()

print("✅ Connected to Ganache blockchain.")

# --- 2. GET YOUR ACCOUNTS FROM GANACHE ---
# Get the list of "demo" accounts Ganache created for you
accounts = web3.eth.accounts
sender_account = accounts[0]
receiver_account = accounts[1]

print(f"   > Using sender account: {sender_account}")

# --- 3. THIS IS YOUR AUDIT DATA (FROM YOUR LAST STEP!) ---
# This is the "proof" we want to save.
audit_results = {
    "document_name": "sample_3.docx",
    "rent_extracted": "Rs. 28,000",
    "deposit_extracted": "Rs. 150,000", # The value you entered
    "state_detected": "Karnataka",
    "stamp_duty_calculated": "Rs. 500.00",
    "audit_status": "SUCCESS"
}

# We must convert our Python dictionary to a JSON string to send it
data_to_log = json.dumps(audit_results)
print(f"   > Logging this data: {data_to_log}")


# --- 4. CREATE AND SEND THE TRANSACTION ---
# This is the final step. We send a transaction with our audit data
# attached as "data".
try:
    tx_hash = web3.eth.send_transaction({
        'from': sender_account,
        'to': receiver_account,
        'value': 0, # We aren't sending money, just data
        'data': data_to_log.encode('utf-8').hex() # Encode our data
    })

    print("\n---  SUCCESS! AUDIT TRAIL CREATED ---")
    print(f"Your immutable proof is this Transaction Hash:")
    print(f"{tx_hash.hex()}")
    
    print("\n(You can now look at the 'TRANSACTIONS' tab in Ganache to see this!)")

except Exception as e:
    print(f"\n---  ERROR ---")
    print(f"Transaction failed: {e}")
    print("This usually happens if you reset Ganache. Try restarting Ganache and run this script again.")