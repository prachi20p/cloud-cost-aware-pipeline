regions = {
    "us-east-1": 0.10,
    "us-west-2": 0.12,
    "ap-south-1": 0.09
}

cheapest = min(regions, key=regions.get)
highest = max(regions, key=regions.get)

savings = regions[highest] - regions[cheapest]

html = "<h1>Cloud Cost-Aware Deployment</h1>"
html += "<h2>Region Price Comparison</h2><ul>"

for r, cost in regions.items():
    html += f"<li>{r}: ${cost}/hour</li>"

html += "</ul>"
html += f"<p><b>Chosen Region:</b> {cheapest}</p>"
html += f"<p><b>Estimated Savings:</b> ${savings:.2f}/hour</p>"

with open("index.html", "w") as f:
    f.write(html)

print("Website updated with cost comparison.")