from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import uuid
import os

from app.utils.report_logic import generate_report

app = FastAPI()

# In-memory tracking of reports
reports = {}

@app.post("/trigger_report")
def trigger_report(background_tasks: BackgroundTasks):
    # Generate a unique report_id
    report_id = str(uuid.uuid4())

    # Mark the report as running
    reports[report_id] = "Running"

    # Launch report generation in background
    background_tasks.add_task(run_report, report_id)

    return {"report_id": report_id}

def run_report(report_id):
    try:
        generate_report(report_id)
        reports[report_id] = "Complete"
    except Exception as e:
        reports[report_id] = f"Failed: {str(e)}"

@app.get("/get_report")
def get_report(report_id: str):
    if report_id not in reports:
        raise HTTPException(status_code=404, detail="Report ID not found")

    status = reports[report_id]

    if status == "Running":
        return {"status": "Running"}
    elif status.startswith("Failed"):
        return {"status": "Failed", "error": status}
    elif status == "Complete":
        filepath = f"output/{report_id}.csv"
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Report file not found")
        return FileResponse(filepath, media_type='text/csv', filename=f"{report_id}.csv")
    else:
        raise HTTPException(status_code=400, detail="Unknown status")
