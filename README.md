### 🏪 Store Monitoring - Take Home Assignment

## 🧩 Data Sources Provided
Store Status CSV — store_id, timestamp_utc, status (active/inactive)

Business Hours CSV — store_id, dayOfWeek (0=Monday), start_time_local, end_time_local

Timezones CSV — store_id, timezone_str

## Project Structure 
``` 
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

## 🛠️ Tech Stack
Python 3.9+

FastAPI (for API building)

SQLAlchemy (ORM)

Pandas (data processing)

Pytz (timezone conversion)

## ⚙️ How the System Works
Database stores all CSV data.

API /trigger_report triggers the calculation process.

API /get_report allows users to download the final report when ready.

Uptime/Downtime is calculated only within business hours using timezone-aware logic.

Gaps between polling data are handled using the last known status for interpolation.

Reports are dynamically generated based on current database data, not hardcoded.

## 📈 Report Output Schema
The generated CSV report contains:


## Column	Meaning
store_id	Store UUID
uptime_last_hour(min)	Uptime during last hour (minutes)
downtime_last_hour(min)	Downtime during last hour (minutes)
uptime_last_day(min)	Uptime during last 24 hours (minutes)
downtime_last_day(min)	Downtime during last 24 hours (minutes)
uptime_last_week(min)	Uptime during last 7 days (minutes)
downtime_last_week(min)	Downtime during last 7 days (minutes)

## 🧠 Understanding the Calculation Logic
Timestamps are converted from UTC to local timezone using the store's timezone_str.

If timezone data is missing, default timezone used: America/Chicago.

If business hours are missing, default assumption: 24x7 open.

Minute-level interpolation is applied between polling times.

Only timestamps within business hours are considered for uptime/downtime.

No precomputation — live dynamic generation based on database data.

## 🎥 Demo Video
[Loom Video Link - Insert your recording link here 🔗]

## 📁 Sample Output
[Google Drive Sample Report Link - Insert your CSV link here 📄]

## 💡 Ideas for Future Improvement
Move report generation to background tasks using Celery or FastAPI BackgroundTasks.

Add Pagination if the number of stores exceeds 10,000+.

Implement User Authentication and API Token Security.

Add Trend Graphs (Matplotlib/Plotly) for visualization.

Package project using Docker for easier deployment.

## 📜 Important Notes
This project is designed for the assignment evaluation only.
Only 10 stores are added in the output for fast evaluation.
