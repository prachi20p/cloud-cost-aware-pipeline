import boto3
import json
import psutil
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
pricing = boto3.client("pricing", region_name="us-east-1")

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
    price_dimensions = next(iter(terms["priceDimensions"].values()))
    return float(price_dimensions["pricePerUnit"]["USD"])


regions_map = {
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
    "ap-south-1": "Asia Pacific (Mumbai)",
}

prices = {r: get_price(loc) for r, loc in regions_map.items()}

current_region = "us-east-1"
cheapest_region = min(prices, key=prices.get)

current_price = prices[current_region]
cheapest_price = prices[cheapest_region]

savings = current_price - cheapest_price

# --- CPU Monitoring ---
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent

html = f"""
<h1>Real AWS Cost Dashboard</h1>

<h2>💰 Pricing Info</h2>
<p>Current Region: {current_region} (${current_price}/hour)</p>
<p>Cheapest Region: {cheapest_region} (${cheapest_price}/hour)</p>
<p>Estimated Savings: ${savings:.4f}/hour</p>

<h2>🖥 Server Usage</h2>
<p>CPU Usage: {cpu_usage}%</p>
<p>Memory Usage: {memory_usage}%</p>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Dashboard updated with pricing and CPU stats.")