### 🏪 Store Monitoring - Take Home Assignment

## 📜 Problem Overview
Loop monitors several restaurants across the US and needs to generate uptime/downtime reports based on the restaurant's business hours and operational status.

This project provides backend APIs that:

Store operational data into a database

Allow users to trigger a report generation

Allow users to poll report status and download the result

## 🧩 Data Sources Provided
Store Status CSV — store_id, timestamp_utc, status (active/inactive)

Business Hours CSV — store_id, dayOfWeek (0=Monday), start_time_local, end_time_local

Timezones CSV — store_id, timezone_str

## 🛠️ Tech Stack
Python 3.9+

FastAPI (for API building)

SQLAlchemy (ORM)

Pandas (data processing)

Pytz (timezone conversion)

## 🚀 System Features
✅ Ingest CSV data into database

✅ Extrapolate store status based on limited polling

✅ Calculate uptime and downtime:

In last hour (minutes)

In last day (hours)

In last week (hours)

✅ Handle missing data:

Assume 24x7 open if no business hours provided

Assume America/Chicago if timezone missing

✅ Provide two APIs:

/trigger_report

/get_report

✅ Save report CSV into output/ folder

📂 Project Structure
``` bash

app/
 ├── db/
 │     ├── database.py       # Database connection setup
 │     ├── models.py         # ORM models (StoreStatus, BusinessHours, Timezones)
 │     └── seed_data.py      # Script to seed initial CSV data into the database
 ├── utils/
 │     └── report_logic.py   # Core logic for report generation
 ├── api/
 │     └── report.py         # API endpoints: trigger_report, get_report
 ├── data/
 │     └── sample.csv        # Sample input CSV files (status, business hours, timezone)
output/
 └── store_report.csv # (Generated uptime/downtime report)
README.md                    # Project documentation
``` 

## 📊 API Specification
1. /trigger_report
Method: POST

Input: None

Output: Returns a unique report_id

Behavior: Starts generating the report asynchronously.

Example Response:

json
{
  "report_id": "8f5d9f2e-3a64-4b2c-92aa-3c934ff9c64d"
}

2. /get_report
Method: GET

Input: report_id

Output: Status or CSV download

Behavior:

If report is running: "status": "Running"

If report is ready: returns "status": "Complete" + download link.

Example Response:

json
{
  "status": "Complete",
  "download_url": "/download/store_uptime_report.csv"
}

## 📊 Sample CSV Output (Schema)

store_id	uptime_last_hour(min)	downtime_last_hour(min)	uptime_last_day(min)	downtime_last_day(min)	uptime_last_week(min)	downtime_last_week(min)
7a242d0e-309c-4915-9755-e9019d69108d	0	0	0	1050	0	7350
...	...	...	...	...	...	...
## 🧪 How to Run Locally
Clone the repo

``` bash
git clone https://github.com/your-username/store-monitoring-assignment.git
cd store-monitoring-assignment
Install Python requirements
``` 
``` bash
pip install -r requirements.txt
Setup your database inside app/db/database.py.
``` 
Run the FastAPI server

``` bash
uvicorn app.api.endpoints:app --reload
Trigger APIs from Postman / Curl / Swagger UI (localhost:8000/docs).
``` 
## 📈 Understanding the Calculation Logic
Business hours and store status are aligned by converting timestamps into local timezone.

If a store has gaps between polling records, sane interpolation is done by assuming the last known status.

Only periods within business hours are counted.

Reports are dynamically generated from database, not hardcoded.

🎥 Demo Video
📺 Loom Recording Link (replace with your final recording)

📁 Sample Report File
📄 Sample CSV Output (Google Drive) (replace with your actual upload)

💡 Ideas for Improvement
Move background report generation to Celery or FastAPI background tasks.

Pagination support if stores >10k+.

Full user authentication and API token security.

Generate trend graphs using Matplotlib/Plotly.

Use Docker to package and deploy easily.
