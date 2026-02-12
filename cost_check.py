regions = {
    "us-east-1": 0.10,
    "us-west-2": 0.12,
    "ap-south-1": 0.09
}

current_region = "us-east-1"
cheapest_region = min(regions, key=regions.get)

current_price = regions[current_region]
cheapest_price = regions[cheapest_region]
savings = current_price - cheapest_price

html = """
<html>
<head>
<title>Cloud Cost Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h1>Cloud Cost-Aware Deployment Dashboard</h1>

<p><b>Current Region:</b> %s ($%.2f/hour)</p>
<p><b>Chosen Region:</b> %s ($%.2f/hour)</p>
<p><b>Estimated Savings:</b> $%.2f/hour</p>

<canvas id="costChart" width="400" height="200"></canvas>

<script>
const ctx = document.getElementById('costChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: %s,
        datasets: [{
            label: 'Cost per Hour ($)',
            data: %s,
            backgroundColor: 'skyblue'
        }]
    }
});
</script>

</body>
</html>
""" % (
    current_region,
    current_price,
    cheapest_region,
    cheapest_price,
    savings,
    list(regions.keys()),
    list(regions.values())
)

with open("index.html", "w") as f:
    f.write(html)

print("Dashboard updated.")