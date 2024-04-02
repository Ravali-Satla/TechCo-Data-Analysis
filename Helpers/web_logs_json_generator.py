import json
from datetime import datetime, timedelta
import random

# Generate JSON records
records = []

for log_id in range(1, 501):
    timestamp = (datetime.strptime("2023-08-02 10:30:45", "%Y-%m-%d %H:%M:%S") + timedelta(minutes=random.randint(1, 10000))).strftime("%Y-%m-%d %H:%M:%S")
    customer_id = f"CUST{log_id}"
    product_id = f"PROD{log_id % 10:03d}"
    action = random.choice(["view", "add_to_cart", "purchase"])
    quantity = None if action == "view" else random.randint(1, 10)
    
    record = {
        "log_id": log_id,
        "timestamp": timestamp,
        "customer_id": customer_id,
        "product_id": product_id,
        "action": action,
        "quantity": quantity
    }
    
    records.append(record)

# Save records to a JSON file
with open("generated_records.json", "w") as json_file:
    json.dump(records, json_file, indent=2)
