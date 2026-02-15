# Cloud Cost-Aware Deployment Dashboard

A real-time dashboard that monitors cloud resource usage (CPU, Memory, Traffic) and provides cost-aware deployment recommendations. This project simulates a multi-region cloud environment and suggests optimal regions based on pricing and performance metrics.

## Features

- **Real-time Monitoring**: Visualize CPU, Memory, and Traffic usage across simulated projects.
- **Cost Analysis**: Track current costs and compare them with optimal region pricing.
- **Predictive Analytics**: Forecast future costs and traffic trends using simulated AI predictions.
- **Region Optimization**: Automatically recommends the most cost-effective region for deployment.
- **Alert System**: Notifications for high CPU usage, cost spikes, and migration recommendations.

## Tech Stack

- **Backend**: Python (Boto3, psutil)
- **Frontend**: HTML5, JavaScript (Chart.js)
- **Containerization**: Docker
- **Cloud Integration**: AWS (Boto3 for pricing API)

## Prerequisites

- [Docker](https://www.docker.com/) installed
- [Python 3.x](https://www.python.org/) installed
- AWS Credentials (if running with live AWS services, though this project uses simulation)

## Installation & Running

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cloud-project/cloud-cost-aware-pipeline
   ```

2. **Run the application using Docker:**
   ```bash
   ./deploy.sh
   # This script pulls changes, stops existing containers, and starts a new Nginx container serving the dashboard.
   ```

3. **Run the data generator (backend simulation):**
   ```bash
   python3 cost_check.py
   # This script generates real-time data and updates the JSON files in the `data/` directory.
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to `http://localhost`.

## Project Structure

- `app.py`: Main application entry point (if applicable).
- `cost_check.py`: Python script simulating cloud metrics and cost calculations.
- `index.html`: Frontend dashboard for visualizing data.
- `deploy.sh`: Shell script for deploying the application via Docker.
- `data/`: Directory storing generated JSON data files.

## License

This project is open-source and available under the content license.
