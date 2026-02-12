import boto3
import json

# AWS pricing client
pricing = boto3.client("pricing", region_name="us-east-1")

# Fetch EC2 price
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

# Region mapping
regions_map = {
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
    "ap-south-1": "Asia Pacific (Mumbai)",
}

# Fetch real prices
prices = {region: get_price(loc) for region, loc in regions_map.items()}

# Current deployment region
current_region = "us-east-1"

# Cheapest region
cheapest_region = min(prices, key=prices.get)

current_price = prices[current_region]
cheapest_price = prices[cheapest_region]

hourly_savings = current_price - cheapest_price

# Monthly estimation
HOURS_PER_DAY = 24
DAYS_PER_MONTH = 30

current_monthly = current_price * HOURS_PER_DAY * DAYS_PER_MONTH
cheapest_monthly = cheapest_price * HOURS_PER_DAY * DAYS_PER_MONTH
monthly_savings = current_monthly - cheapest_monthly

# Generate dashboard HTML
html = f"""
<html>
<head>
<title>Real AWS Cost Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
<h1>Real AWS Deployment Cost Dashboard</h1>

<h2>Deployment Details</h2>
<p><b>Current Region:</b> {current_region}</p>
<p><b>Current Cost:</b> ${current_price:.5f}/hour</p>

<p><b>Cheapest Region:</b> {cheapest_region}</p>
<p><b>Cheapest Cost:</b> ${cheapest_price:.5f}/hour</p>

<p><b>Hourly Savings:</b> ${hourly_savings:.5f}</p>

<h2>Monthly Cost Estimation</h2>
<p>Current Monthly Cost: ${current_monthly:.2f}</p>
<p>Optimized Monthly Cost: ${cheapest_monthly:.2f}</p>
<p><b>Monthly Savings: ${monthly_savings:.2f}</b></p>

<h2>Region Price Comparison</h2>
<canvas id="costChart" width="400" height="200"></canvas>

<script>
const ctx = document.getElementById('costChart').getContext('2d');

new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: {list(prices.keys())},
        datasets: [{{
            label: 'Cost per Hour ($)',
            data: {list(prices.values())},
            backgroundColor: 'skyblue'
        }}]
    }}
}});
</script>

</body>
</html>
"""

# Write dashboard file
with open("index.html", "w") as f:
    f.write(html)

print("Real AWS pricing dashboard updated.")