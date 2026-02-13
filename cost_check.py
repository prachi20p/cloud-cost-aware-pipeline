import boto3
import json
import psutil
import random
import os
import time

# ---------- Setup ----------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

pricing = boto3.client("pricing", region_name="us-east-1")

# Pricing-compatible regions
pricing_locations = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "eu-west-1": "EU (Ireland)",
    "eu-central-1": "EU (Frankfurt)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-northeast-1": "Asia Pacific (Tokyo)"
}

# ---------- Pricing Fetch ----------
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
        return 999  # fallback

prices = {r: get_price(loc) for r, loc in pricing_locations.items()}

# ---------- Monitoring ----------
cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent

# Traffic simulation
traffic = random.randint(50, 500)

# ---------- Deployment Decision ----------
current_region = "us-east-1"
cheapest_region = min(prices, key=prices.get)

current_price = prices[current_region]
cheapest_price = prices[cheapest_region]

# Region decision
if cpu > 70 or traffic > 400:
    best_region = cheapest_region
else:
    best_region = current_region

best_price = prices[best_region]

status = (
    f"Migrating workload to {best_region}"
    if best_region != current_region
    else "Running optimally"
)

# ---------- Auto Scaling ----------
if cpu > 75 or traffic > 400:
    instances = 4
elif cpu > 55 or traffic > 250:
    instances = 3
elif cpu > 35:
    instances = 2
else:
    instances = 1

# ---------- Cost Prediction ----------
monthly_cost = current_price * 24 * 30
yearly_cost = monthly_cost * 12

# ---------- Multi‑Project Simulation ----------
projects = ["projectA", "projectB", "projectC"]

for project in projects:

    # Slight variation per project
    proj_cpu = min(100, cpu + random.randint(-10, 10))
    proj_mem = min(100, memory + random.randint(-10, 10))
    proj_traffic = max(50, traffic + random.randint(-50, 50))

    data = {
        "project": project,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "current_region": current_region,
        "current_price": current_price,
        "best_region": best_region,
        "best_price": best_price,
        "savings": current_price - best_price,
        "cpu": proj_cpu,
        "memory": proj_mem,
        "traffic": proj_traffic,
        "instances": instances,
        "status": status,
        "monthly_cost": monthly_cost,
        "yearly_cost": yearly_cost,
    }

    with open(f"{DATA_DIR}/{project}.json", "w") as f:
        json.dump(data, f, indent=2)

# ---------- Project List ----------
with open(f"{DATA_DIR}/projects.json", "w") as f:
    json.dump(projects, f)

print("All project dashboards updated successfully.")