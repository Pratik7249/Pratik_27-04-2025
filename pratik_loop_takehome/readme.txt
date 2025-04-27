Store Monitoring Backend System
This is a FastAPI backend service to monitor the uptime and downtime of restaurants based on their business hours and activity status.

📦 Project Structure
bash
Copy
Edit
pratik_loop_takehome/
│
├── app/
│   ├── api/
│   │   └── report_api.py       # API endpoints (trigger_report, get_report)
│   ├── core/
│   ├── data/
│   ├── db/
│   ├── utils/
│   │   └── report_logic.py      # Core report generation logic
│   └── main.py                  # FastAPI application entrypoint
│
├── output/                      # Stores generated report CSVs
├── initialize.py                # Initial database setup
├── loop.db                      # Database file
├── stores.db                    # Backup database
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
🚀 How to Run
1. Clone the Repository
bash
Copy
Edit
git clone <your-repo-url>
cd pratik_loop_takehome
2. Create Virtual Environment and Install Dependencies
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate    # (Linux/macOS)
.venv\Scripts\activate       # (Windows)

pip install -r requirements.txt
3. Initialize the Database
bash
Copy
Edit
python initialize.py
(This step will load all CSVs into the database.)

4. Start the Server
bash
Copy
Edit
uvicorn app.main:app --reload
The server will start at:

http://127.0.0.1:8000

📬 API Endpoints
➡️ 1. Trigger Report
POST /trigger_report

No input body

Response:

json
Copy
Edit
{
  "report_id": "generated-uuid-string"
}
➡️ 2. Get Report
GET /get_report/{report_id}

Response if still processing:

json
Copy
Edit
{
  "status": "Running"
}
Response if completed:

json
Copy
Edit
{
  "status": "Complete",
  "csv_file": "output/{report_id}.csv"
}
📊 Sample Output CSV Schema

store_id	uptime_last_hour(min)	downtime_last_hour(min)	uptime_last_day(min)	downtime_last_day(min)	uptime_last_week(min)	downtime_last_week(min)
1	10	50	10	1430	10	10070
📌 Notes
Business hours missing ➔ assume 24x7 open.

Timezone missing ➔ assume America/Chicago.

Data processed only within business hours.

Interpolates uptime/downtime from hourly pings.

Built with
FastAPI 

SQLite 

Pandas 

Uvicorn 

Author
Name: Pratik

Assignment: Loop Health - Store Monitoring Backend











