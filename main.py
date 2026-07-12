from fastapi import FastAPI, HTTPException, status, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import database

# Initialize Database tables
database.init_db()

app = FastAPI(
    title="AAS Air Conditioning and Engineering API",
    description="Enterprise B2B static site serving and request tracking backend.",
    version="1.0.0"
)

# Admin Key Security Token
ADMIN_SECURE_TOKEN = "AAS_ADMIN_2026"

# --- Pydantic Validation Models ---
class InquirySchema(BaseModel):
    name: str
    company: str
    email: str
    phone: str
    city: str
    product: str
    message: str

class CatalogDownloadSchema(BaseModel):
    email: str

class ChatSchema(BaseModel):
    message: str

# Helper to verify token from Authorization header (Bearer <token>)
def verify_auth_token(authorization: Optional[str] = Header(None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    
    if token != ADMIN_SECURE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access. Invalid admin key."
        )

# --- API Endpoints ---

@app.post("/api/inquiry", status_code=status.HTTP_201_CREATED)
def create_inquiry(payload: InquirySchema):
    try:
        row_id = database.add_inquiry(
            name=payload.name,
            company=payload.company,
            email=payload.email,
            phone=payload.phone,
            city=payload.city,
            product=payload.product,
            message=payload.message
        )
        return {"status": "success", "id": row_id, "message": "Inquiry recorded successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database insertion failed: {str(e)}"
        )

@app.get("/api/inquiries", response_model=List[dict])
def list_inquiries(authorization: Optional[str] = Header(None)):
    verify_auth_token(authorization)
    try:
        return database.get_inquiries()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve inquiries: {str(e)}"
        )

@app.post("/api/catalog-download", status_code=status.HTTP_201_CREATED)
def record_catalog_download(payload: CatalogDownloadSchema):
    try:
        database.add_catalog_download(email=payload.email)
        return {"status": "success", "message": "Catalog download registered."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database insertion failed: {str(e)}"
        )

@app.get("/api/catalog-downloads", response_model=List[dict])
def list_catalog_downloads(authorization: Optional[str] = Header(None)):
    verify_auth_token(authorization)
    try:
        return database.get_catalog_downloads()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve catalog downloads: {str(e)}"
        )

@app.post("/api/chat")
def handle_chat_message(payload: ChatSchema):
    user_msg = payload.message.strip()
    if not user_msg:
        return {"response": "Please enter a valid query."}
    
    lower = user_msg.lower()
    
    # Backend Smart Assistant Parsing Logic
    bot_response = ""
    if "chiller" in lower or "cooling" in lower:
        bot_response = (
            "<strong>AAS Chiller portfolio details:</strong><br>"
            "• <strong>Inverter Chillers:</strong> Ideal for energy savings (reduces annual cost up to 40% using dynamic variable frequency drives).<br>"
            "• <strong>Screw Chillers:</strong> Engineered with reliable European compressors (DX/Flooded versions tested to ARI standards).<br>"
            "• <strong>Scroll Chillers:</strong> Built-in pump and steel buffer tank for modular, plug-and-play operations."
        )
    elif "milk" in lower or "bmc" in lower or "dairy" in lower:
        bot_response = (
            "<strong>AAS Bulk Milk Coolers:</strong> Built in capacities from <strong>500L to 5,000L</strong>. "
            "Features food-grade AISI-304 Stainless Steel panels, thick polyurethane insulation, heavy duty gear agitating, "
            "and built-in digital anti-freezing protections."
        )
    elif "cold" in lower or "puf" in lower or "store" in lower or "room" in lower:
        bot_response = (
            "<strong>AAS Modular Cold Storage:</strong> Available with operating temperatures from <strong>-4°C to 18°C</strong>. "
            "We construct them using high-density PUF panels with G.I. painted outer layer. Features magnetic gasket safety doors."
        )
    elif "washer" in lower or "evaporative" in lower or "humid" in lower:
        bot_response = (
            "<strong>AAS Air Washers & Pressurization:</strong> High-efficiency evaporative units using cross-corrugated "
            "cellulose pads and dynamically balanced fan blowers. Recommended for kitchens, auditoriums, and factory spaces."
        )
    elif "ahu" in lower or "handling" in lower:
        bot_response = (
            "<strong>AAS Air Handling Units:</strong> Heavy-duty double skinned modular configurations available for ceiling suspended "
            "or floor-mounted designs. Configured with imported self-aligning pillow blocks and G.I. wiremesh filter grids."
        )
    elif "address" in lower or "phone" in lower or "contact" in lower or "office" in lower or "number" in lower:
        bot_response = (
            "<strong>AAS Corporate Office:</strong> Plot No. 14, Gali No. 1, Block-A, Nangla Enclave, Part-II, NIT Faridabad, Haryana - 121005 (INDIA).<br>"
            "<strong>Phones:</strong> +91-129-2470786, +91-9999404742<br>"
            "<strong>Email:</strong> info@aasgroups.com"
        )
    elif "laser" in lower or "cnc" in lower or "welding" in lower or "fabrication" in lower:
        bot_response = (
            "<strong>AAS Manufacturing Power:</strong> Our NIT Faridabad facility utilizes 16mm CNC fiber laser cutters, "
            "automated duct rolling presses matching SMACNA class standards, and certified nitrogen joints check stands."
        )
    elif "price" in lower or "quote" in lower or "cost" in lower:
        bot_response = (
            "We offer custom commercial pricing based on capacities (TR) and fluid types. Please fill out our "
            "<strong>Request Quote form</strong> or email us at <strong>info@aasgroups.com</strong> with your parameters for a detailed budget proposal."
        )
    else:
        bot_response = (
            "Thank you for reaching out to AAS Air Conditioning & Engineering! Your message is logged. For complex drawings "
            "or tender document reviews, our corporate line is available at <strong>+91-9999404742</strong>."
        )
        
    try:
        database.add_chat(user_message=user_msg, bot_response=bot_response)
    except:
        pass
        
    return {"response": bot_response}

@app.get("/api/chats", response_model=List[dict])
def list_chats(authorization: Optional[str] = Header(None)):
    verify_auth_token(authorization)
    try:
        return database.get_chats()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve chat logs: {str(e)}"
        )

# --- Serving Static Frontend ---
static_dir = os.path.join(os.path.dirname(__file__), 'static')

# Serve admin.html on '/admin' (Must be declared before root mounting to avoid masking)
@app.get("/admin")
def serve_admin():
    return FileResponse(os.path.join(static_dir, 'admin.html'))

# Mount the static directory directly at root '/'
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
