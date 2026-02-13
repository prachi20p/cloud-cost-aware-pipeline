import boto3
import json
import psutil
import random
import os
import time

DATA_DIR = "data"
HISTORY_DIR = f"{DATA_DIR}/history"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

pricing = boto3.client("pricing", region_name="us-east-1")

pricing_locations = {
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
    "eu-west-1": "EU (Ireland)",
    "ap-south-1": "Asia Pacific (Mumbai)",
}

def get_price(region_location):
    try:
        response = pricing.get_products(
            ServiceCode="AmazonEC2",
            Filters=[
                {"Type": "TERM_MATCH", "Field": "instanceType", "Value": "t2.micro"},
                {"Type": "TERM_MATCH", "Field": "location", "Value": region_location},
                {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
            ],
            MaxResults=1,
        )

        price_item = json.loads(response["PriceList"][0])
        terms = next(iter(price_item["terms"]["OnDemand"].values()))
        dims = next(iter(terms["priceDimensions"].values()))
        return float(dims["pricePerUnit"]["USD"])
    except Exception:
        return 999

prices = {r: get_price(loc) for r, loc in pricing_locations.items()}

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent
traffic = random.randint(50, 500)

current_region = "us-east-1"
best_region = min(prices, key=prices.get)

current_price = prices[current_region]
best_price = prices[best_region]

status = (
    f"Migrating workload to {best_region}"
    if best_region != current_region
    else "Running optimally"
)

if cpu > 75 or traffic > 400:
    instances = 4
elif cpu > 55:
    instances = 3
elif cpu > 35:
    instances = 2
else:
    instances = 1

monthly_cost = current_price * 24 * 30

forecast_next_month = monthly_cost * random.uniform(0.9, 1.2)
forecast_two_month = forecast_next_month * random.uniform(0.9, 1.15)
forecast_three_month = forecast_two_month * random.uniform(0.9, 1.15)

projects = ["projectA", "projectB", "projectC"]

for project in projects:

    proj_cpu = max(1, min(100, cpu + random.randint(-10, 10)))
    proj_mem = max(1, min(100, memory + random.randint(-10, 10)))
    proj_traffic = max(50, traffic + random.randint(-50, 50))

    project_data = {
        "project": project,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "current_region": current_region,
        "best_region": best_region,
        "current_price": current_price,
        "cpu": proj_cpu,
        "memory": proj_mem,
        "traffic": proj_traffic,
        "instances": instances,
        "status": status,
        "monthly_cost": monthly_cost,
        "forecast": [
            monthly_cost,
            forecast_next_month,
            forecast_two_month,
            forecast_three_month
        ]
    }

    with open(f"{DATA_DIR}/{project}.json", "w") as f:
        json.dump(project_data, f, indent=2)

    history_file = f"{HISTORY_DIR}/{project}.json"

    record = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": proj_cpu,
        "memory": proj_mem,
        "traffic": proj_traffic,
        "instances": instances,
        "cost": current_price
    }

    history = []
    if os.path.exists(history_file):
        with open(history_file) as f:
            history = json.load(f)

    history.append(record)
    history = history[-200:]

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

with open(f"{DATA_DIR}/projects.json", "w") as f:
    json.dump(projects, f)

print("Phase 14 analytics updated.")
