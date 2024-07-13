# Salesman Scheduler

## Overview
Salesman Scheduler is a Python-based project designed to help insurance salespeople optimize their travel routes and schedule meetings efficiently. The application reads customer data from a CSV file, converts addresses to geographical coordinates, calculates the optimal travel route using the Traveling Salesman Algorithm, and integrates the meeting schedule with Google Calendar.

## Features
- Reads customer data from a CSV file
- Geocodes addresses to get geographical coordinates
- Calculates distances between locations in kilometers
- Optimizes travel route using the Traveling Salesman Algorithm
- Schedules meetings and integrates them with Google Calendar
- Supports setting meeting times in Indian Standard Time (IST)

## Prerequisites
- Python 3.6+
- Required Python packages:
  - `geopy`
  - `haversine`
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/salesman-scheduler.git
    ```
2. Navigate to the project directory:
    ```sh
    cd salesman-scheduler
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration
1. Obtain your Google Calendar API credentials:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Enable the Google Calendar API for the project.
    - Create OAuth 2.0 credentials and download the `credentials.json` file.

2. Place the `credentials.json` file in the project directory.

## Usage
1. Prepare your customer data CSV file with the following columns: `name`, `address`, `zip`.

2. Update the `file_path` variable in the `sales.py` script with the path to your CSV file.

3. Run the script:
    ```sh
    python sales.py
    ```

## Example
Here's an example of what the customer data CSV file (`smp_address_dataset.csv`) should look like:

```csv
name,address,zip
John Doe,123 Main St,12345
Jane Smith,456 Oak St,67890
...
