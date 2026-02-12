import boto3
import json

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

html = f"""
<h1>Real AWS Cost Dashboard</h1>
<p>Current Region: {current_region} (${current_price}/hour)</p>
<p>Cheapest Region: {cheapest_region} (${cheapest_price}/hour)</p>
<p>Estimated Savings: ${savings:.4f}/hour</p>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Real AWS pricing updated.")