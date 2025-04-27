from fastapi import APIRouter
import uuid
import threading
from app.utils.report_logic import generate_report

router = APIRouter()

report_status = {}

@router.post("/trigger_report")
def trigger_report():
    report_id = str(uuid.uuid4())
    report_status[report_id] = "Running"

    def task():
        generate_report(report_id)
        report_status[report_id] = "Complete"

    threading.Thread(target=task).start()

    return {"report_id": report_id}

@router.get("/get_report/{report_id}")
def get_report(report_id: str):
    status = report_status.get(report_id)
    
    if status is None:
        return {"error": "Invalid report_id"}
    
    if status == "Running":
        return {"status": "Running"}
    
    if status == "Complete":
        return {
            "status": "Complete",
            "csv_file": f"output/{report_id}.csv"
        }
