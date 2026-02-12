# Simulated region prices
regions = {
    "us-east-1": 0.10,
    "us-west-2": 0.12,
    "ap-south-1": 0.09
}

# Simulated current deployment region
current_region = "us-east-1"

# Find cheapest region
cheapest_region = min(regions, key=regions.get)

current_price = regions[current_region]
cheapest_price = regions[cheapest_region]

savings = current_price - cheapest_price

html = "<h1>Cloud Cost-Aware Deployment</h1>"

html += "<h2>Deployment Details</h2>"
html += f"<p><b>Current Region:</b> {current_region}</p>"
html += f"<p><b>Current Region Cost:</b> ${current_price}/hour</p>"

html += f"<p><b>Chosen Region:</b> {cheapest_region}</p>"
html += f"<p><b>Chosen Region Cost:</b> ${cheapest_price}/hour</p>"

html += f"<p><b>Estimated Savings:</b> ${savings:.2f}/hour</p>"

html += "<h2>All Region Prices</h2><ul>"
for r, cost in regions.items():
    html += f"<li>{r}: ${cost}/hour</li>"
html += "</ul>"

with open("index.html", "w") as f:
    f.write(html)

print("Website updated with region comparison.")