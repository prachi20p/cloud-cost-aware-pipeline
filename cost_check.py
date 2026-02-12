import random

# Simulated region prices (change randomly to simulate market)
regions = {
    "us-east-1": round(random.uniform(0.09, 0.13), 2),
    "us-west-2": round(random.uniform(0.09, 0.13), 2),
    "ap-south-1": round(random.uniform(0.08, 0.12), 2)
}

# Simulated current deployment
current_region = "us-east-1"

cheapest_region = min(regions, key=regions.get)

current_price = regions[current_region]
cheapest_price = regions[cheapest_region]

savings = current_price - cheapest_price

migration_needed = cheapest_region != current_region

decision = (
    f"Migrate deployment to {cheapest_region}"
    if migration_needed
    else "Deployment already optimal"
)

html = f"""
<html>
<head>
<title>Cloud Deployment Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h1>Multi‑Region Deployment Simulation</h1>

<p><b>Current Region:</b> {current_region} (${current_price}/hour)</p>
<p><b>Cheapest Region:</b> {cheapest_region} (${cheapest_price}/hour)</p>
<p><b>Estimated Savings:</b> ${savings:.2f}/hour</p>
<p><b>Deployment Decision:</b> {decision}</p>

<canvas id="costChart"></canvas>

<script>
const ctx = document.getElementById('costChart').getContext('2d');
new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: {list(regions.keys())},
        datasets: [{{
            label: 'Cost per Hour ($)',
            data: {list(regions.values())},
            backgroundColor: 'skyblue'
        }}]
    }}
}});
</script>

</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Deployment simulation updated.")