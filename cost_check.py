import boto3
import json
import psutil

# AWS pricing client
pricing = boto3.client("pricing", region_name="us-east-1")

regions_map = {
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
    "ap-south-1": "Asia Pacific (Mumbai)",
}

def get_price(region_name):
    response = pricing.get_products(
        ServiceCode="AmazonEC2",
        Filters=[
            {"Type": "TERM_MATCH", "Field": "instanceType", "Value": "t2.micro"},
            {"Type": "TERM_MATCH", "Field": "location", "Value": region_name},
            {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
        ],
        MaxResults=1,
    )

    price_item = json.loads(response["PriceList"][0])
    terms = next(iter(price_item["terms"]["OnDemand"].values()))
    dims = next(iter(terms["priceDimensions"].values()))

    return float(dims["pricePerUnit"]["USD"])

# Fetch prices
prices = {r: get_price(loc) for r, loc in regions_map.items()}

# System load
cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent

current_region = "us-east-1"
cheapest_region = min(prices, key=prices.get)

current_price = prices[current_region]
cheapest_price = prices[cheapest_region]

# Load‑aware region decision
if cpu > 70:
    best_region = cheapest_region
else:
    best_region = current_region

best_price = prices[best_region]

# Migration simulation
if best_region != current_region:
    status = f"Migrating workload to {best_region}..."
else:
    status = "Running optimally"

# Auto‑scaling simulation
instances = 1
if cpu > 70:
    instances = 3
elif cpu > 40:
    instances = 2

# Cost prediction
monthly_cost = current_price * 24 * 30
yearly_cost = monthly_cost * 12

# Data output
data = {
    "current_region": current_region,
    "current_price": current_price,
    "best_region": best_region,
    "best_price": best_price,
    "savings": current_price - best_price,
    "cpu": cpu,
    "memory": memory,
    "status": status,
    "instances": instances,
    "monthly_cost": monthly_cost,
    "yearly_cost": yearly_cost,
}

with open("data.json", "w") as f:
    json.dump(data, f)

print("Dashboard data updated.")