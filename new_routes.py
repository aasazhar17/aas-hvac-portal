from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import FileResponse
import csv
import os
import database
from logger import logger
import config

router = APIRouter()

# Helper to verify role from auth token
def verify_role_access(authorization: str, allowed_roles: list) -> str:
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        
    if token == config.ADMIN_PASSKEY:
        role = "admin"
    elif token == config.SALES_PASSKEY:
        role = "sales"
    elif token == config.EDITOR_PASSKEY:
        role = "editor"
    else:
        logger.warning("Failed authentication attempt using invalid passkey.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passkey authorization."
        )
        
    if role not in allowed_roles:
        logger.warning(f"Unauthorized role access attempt: role={role} tried to access restricted route.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Insufficient permissions."
        )
    return role

@router.get("/admin/export-csv")
def export_csv(authorization: str = Header(...)):
    verify_role_access(authorization, ["admin", "sales"])
    logger.info("CSV Leads export requested by authorized admin/sales.")
    
    try:
        inquiries = database.get_inquiries()
        csv_file_path = os.path.join(os.path.dirname(__file__), "static", "leads.csv")
        
        # Write inquires to CSV
        with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Timestamp", "Name", "Company", "Email", "Phone", "City", "Product Interest", "Message"])
            for inq in inquiries:
                writer.writerow([
                    inq.get("id"),
                    inq.get("created_at"),
                    inq.get("name"),
                    inq.get("company"),
                    inq.get("email"),
                    inq.get("phone"),
                    inq.get("city"),
                    inq.get("product"),
                    inq.get("message")
                ])
                
        return FileResponse(
            path=csv_file_path,
            filename="aas_inquiries_leads.csv",
            media_type="text/csv"
        )
    except Exception as e:
        logger.error(f"Failed to generate CSV export file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate CSV: {str(e)}"
        )

@router.get("/admin/backup-db")
def backup_database(authorization: str = Header(...)):
    verify_role_access(authorization, ["admin"])
    logger.info("Database backup requested by authorized Super Admin.")
    
    db_file_path = database.DATABASE_FILE
    if not os.path.exists(db_file_path):
        logger.error(f"Active database file not found for backup: path={db_file_path}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database file not found."
        )
        
    return FileResponse(
        path=db_file_path,
        filename="aas_database_backup.db",
        media_type="application/octet-stream"
    )

@router.get("/api/chart-data")
def get_chart_data():
    # Public route, utilized by admin JS once logged in
    logger.info("Fetched chart analytics data points.")
    try:
        inquiries = database.get_inquiries()
        from datetime import datetime, timedelta
        
        today = datetime.now()
        dates = []
        counts = []
        
        # Initialize dates dictionary
        date_map = {}
        for i in range(6, -1, -1):
            dt = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            date_map[dt] = 0
            dates.append(dt)
            
        for inq in inquiries:
            created_at = inq.get("created_at", "")
            if len(created_at) >= 10:
                date_str = created_at[:10]
                if date_str in date_map:
                    date_map[date_str] += 1
                    
        for d in dates:
            counts.append(date_map[d])
            
        return {"dates": dates, "counts": counts}
    except Exception as e:
        logger.error(f"Failed to process chart analytics data points: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
