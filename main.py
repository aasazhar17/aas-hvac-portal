from fastapi import FastAPI, HTTPException, status, Header, UploadFile, File, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import os
import database
import config
from logger import logger
import new_routes

# Initialize Database tables
database.init_db()

app = FastAPI(
    title="AAS Air Conditioning and Engineering API",
    description="Enterprise B2B static site serving and request tracking backend with product CRUD and upload support.",
    version="1.1.0"
)

# Include administrative router
app.include_router(new_routes.router)

# Passkey configuration from environment config
ADMIN_PASSKEY = config.ADMIN_PASSKEY
SALES_PASSKEY = config.SALES_PASSKEY
EDITOR_PASSKEY = config.EDITOR_PASSKEY

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

class ProductSchema(BaseModel):
    id: str
    name: str
    category: str
    image: str
    badge: str
    desc: str
    specs: dict

# Helper to verify token and return role
def get_user_role(authorization: Optional[str] = Header(None)) -> str:
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    
    if token == ADMIN_PASSKEY:
        return "admin"
    elif token == SALES_PASSKEY:
        return "sales"
    elif token == EDITOR_PASSKEY:
        return "editor"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access. Invalid passkey credentials."
        )

# --- API Endpoints ---

def send_simulated_email(email: str, name: str):
    logger.info(f"Asynchronous BackgroundTask: Auto-reply confirmation email queued/sent to {name} <{email}>")
    logger.info(f"SMTP SIMULATOR: Auto-reply confirmation email sent to {name} <{email}>")

@app.post("/api/inquiry", status_code=status.HTTP_201_CREATED)
def create_inquiry(payload: InquirySchema, background_tasks: BackgroundTasks):
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
        background_tasks.add_task(send_simulated_email, payload.email, payload.name)
        logger.info(f"Successfully recorded new inquiry lead: id={row_id}, name={payload.name}, company={payload.company}")
        return {"status": "success", "id": row_id, "message": "Inquiry recorded successfully."}
    except Exception as e:
        logger.error(f"Failed to record new inquiry lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database insertion failed: {str(e)}"
        )

@app.get("/api/inquiries", response_model=List[dict])
def list_inquiries(authorization: Optional[str] = Header(None)):
    role = get_user_role(authorization)
    if role not in ["admin", "sales"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Access restricted to Admin or Sales roles."
        )
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
    role = get_user_role(authorization)
    if role not in ["admin", "sales"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Access restricted to Admin or Sales roles."
        )
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
    role = get_user_role(authorization)
    if role not in ["admin", "sales"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Access restricted to Admin or Sales roles."
        )
    try:
        return database.get_chats()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve chat logs: {str(e)}"
        )

# --- Product CRUD API ---

@app.get("/api/products")
def get_all_products():
    try:
        return database.get_products()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not fetch products: {str(e)}"
        )

@app.post("/api/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductSchema, authorization: Optional[str] = Header(None)):
    role = get_user_role(authorization)
    if role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Only Admin or Editor can create products."
        )
    try:
        existing = database.get_product(payload.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product ID already exists."
            )
        database.add_product(
            product_id=payload.id,
            name=payload.name,
            category=payload.category,
            image=payload.image,
            badge=payload.badge,
            desc=payload.desc,
            specs=payload.specs
        )
        return {"status": "success", "message": "Product created successfully."}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )

@app.put("/api/products/{product_id}")
def update_product(product_id: str, payload: ProductSchema, authorization: Optional[str] = Header(None)):
    role = get_user_role(authorization)
    if role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Only Admin or Editor can update products."
        )
    try:
        existing = database.get_product(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )
        database.update_product(
            product_id=product_id,
            name=payload.name,
            category=payload.category,
            image=payload.image,
            badge=payload.badge,
            desc=payload.desc,
            specs=payload.specs
        )
        return {"status": "success", "message": "Product updated successfully."}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )

@app.delete("/api/products/{product_id}")
def delete_product(product_id: str, authorization: Optional[str] = Header(None)):
    role = get_user_role(authorization)
    if role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Only Admin or Editor can delete products."
        )
    try:
        existing = database.get_product(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )
        database.delete_product(product_id)
        return {"status": "success", "message": "Product deleted successfully."}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

# --- Image Upload API ---

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    role = get_user_role(authorization)
    if role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Only Admin or Editor can upload files."
        )
    try:
        file_name = file.filename
        base_name = os.path.basename(file_name)
        images_dir = os.path.join(static_dir, "assets", "images")
        os.makedirs(images_dir, exist_ok=True)
        
        save_path = os.path.join(images_dir, base_name)
        with open(save_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        return {"status": "success", "image_url": f"assets/images/{base_name}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {str(e)}"
        )

# --- Serving Static Frontend ---
static_dir = os.path.join(os.path.dirname(__file__), 'static')

# Jinja2 templates initialization
templates = Jinja2Templates(directory=static_dir)

# Shared SEO context used by the HTML templates

def get_page_context():
    return {
        "default_title": "AAS Air Conditioning & Engineering | Industrial HVAC Faridabad",
        "default_description": "ISO 9001:2015 certified manufacturer of scroll/screw chillers, AHUs, clean rooms, and ventilation systems in India since 2006."
    }

# Exception handlers for error pages
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        logger.warning(f"404 Not Found: path={request.url.path}")
        return templates.TemplateResponse("404.html", {"request": request, **get_page_context()}, status_code=404)
    elif exc.status_code >= 500:
        logger.error(f"HTTP Server Exception: {exc.detail}")
        return templates.TemplateResponse("500.html", {"request": request, **get_page_context()}, status_code=exc.status_code)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)

@app.exception_handler(Exception)
async def custom_generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal 500 Server Exception: {str(exc)}")
    return templates.TemplateResponse("500.html", {"request": request, **get_page_context()}, status_code=500)

# Serve templates for index and admin routes
@app.get("/")
def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, **get_page_context()})

@app.get("/admin")
def serve_admin_portal(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, **get_page_context()})

# Subclass StaticFiles to support max-age cache control headers
class CachingStaticFiles(StaticFiles):
    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "public, max-age=31536000"
        return response

if os.path.exists(static_dir):
    app.mount("/", CachingStaticFiles(directory=static_dir, html=True), name="static")

