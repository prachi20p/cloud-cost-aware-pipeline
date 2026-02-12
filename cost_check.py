regions = {
    "us-east-1": 0.10,
    "us-west-2": 0.12,
    "ap-south-1": 0.09
}

cheapest = min(regions, key=regions.get)

output = f"""
<h1>Cloud Cost-Aware Deployment</h1>
<p>Cheapest Region: {cheapest}</p>
<p>Estimated Cost: ${regions[cheapest]}/hour</p>
"""

with open("index.html", "w") as f:
    f.write(output)

print("Website updated with cheapest region.")
