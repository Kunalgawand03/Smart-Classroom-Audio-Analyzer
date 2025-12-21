# gsheet_reader.py
import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any

# ====== UPDATE THIS PATH ======
# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = r".\keys\gcp-service-account.json"   # <--- change this!

# ====== REQUIRED SCOPES ======
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def open_sheet(sheet_id: str, worksheet_name: str = None):
    """Opens Google Sheet by ID."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_id)

    if worksheet_name:
        ws = sh.worksheet(worksheet_name)
    else:
        ws = sh.sheet1
    return ws

def fetch_latest_metrics(sheet_id: str, worksheet_name: str = None) -> Dict[str, Any]:
    """
    Reads the sheet and returns a dict for the latest non-empty row.
    Expects headers:
    timestamp, class_id, total_students, present_count,
    active_events, total_events, extra_actions, performance
    """
    ws = open_sheet(sheet_id, worksheet_name)
    records = ws.get_all_records()

    if not records:
        raise ValueError("Sheet is empty or headers missing.")

    latest = records[-1]   # last row

    # convert numeric fields safely
    def to_int(x):
        try:
            return int(x)
        except Exception:
            try:
                return int(float(x))
            except Exception:
                return 0

    return {
        "timestamp": latest.get("timestamp"),
        "class_id": latest.get("class_id"),
        "total_students": to_int(latest.get("total_students", 0)),
        "present_count": to_int(latest.get("present_count", 0)),
        "active_events": to_int(latest.get("active_events", 0)),
        "total_events": to_int(latest.get("total_events", 0)),
        "extra_actions": to_int(latest.get("extra_actions", 0)),
        "performance": to_int(latest.get("performance", 0)),
        "raw_row": latest
    }
