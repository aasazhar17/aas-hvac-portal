import sqlite3
import os
import json
from datetime import datetime

DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inquiries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            product TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Catalog downloads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catalog_downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Chat logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            image TEXT NOT NULL,
            badge TEXT NOT NULL,
            desc TEXT NOT NULL,
            specs TEXT NOT NULL
        )
    ''')
    
    conn.commit()

    # Pre-populate products table if it's empty
    cursor.execute('SELECT COUNT(*) FROM products')
    count = cursor.fetchone()[0]
    if count == 0:
        default_products = [
            {
                "id": "screw-chiller",
                "name": "AAS Screw Chiller",
                "category": "chillers",
                "image": "assets/images/chiller.png",
                "badge": "High Capacity",
                "desc": "Designed for uninterruptible industrial operations in extreme tropical climates with capacity control and high-efficiency European screw compressors.",
                "specs": {
                    "Compressor Type": "Reliable European Screw Compressor (ARI tested)",
                    "System Type": "Available in DX (Direct Expansion) & Flooded systems",
                    "Features": "Capacity control, tropicalized condensing unit, eco-friendly refrigerants",
                    "Typical Applications": "Chemical, pharmaceutical, rubber, and heavy process industries"
                }
            },
            {
                "id": "scroll-chiller",
                "name": "AAS Scroll Chiller",
                "category": "chillers",
                "image": "assets/images/chiller.png",
                "badge": "ISO Certified",
                "desc": "Modular scroll chillers configured with integrated water tank and circulation pumps for fast plug-and-play installation.",
                "specs": {
                    "Controls": "Microprocessor-based digital system",
                    "Design Standard": "ISO 9001:2015 certified manufacturing unit",
                    "Configuration": "Built-in storage tank & water circulation pump",
                    "Advantages": "Compact footprint, low noise emissions, easy maintenance"
                }
            },
            {
                "id": "inverter-chiller",
                "name": "AAS Inverter Chiller",
                "category": "chillers",
                "image": "assets/images/chiller.png",
                "badge": "Up to 40% Savings",
                "desc": "Advanced chilling units regulating compressor RPM dynamically to match variable process loads, saving significant energy costs.",
                "specs": {
                    "Technology": "Dynamic frequency drive inverter controls",
                    "Energy Saving": "Up to 40% annual electricity bill reduction",
                    "Startup Current": "Smooth soft-start curve with no heavy current spikes",
                    "Protection": "Under/over voltage and phase loss protection built-in"
                }
            },
            {
                "id": "recip-chiller",
                "name": "AAS Recip Chiller",
                "category": "chillers",
                "image": "assets/images/chiller.png",
                "badge": "Low Maintenance",
                "desc": "Heavy-duty reciprocating compressor chillers designed to withstand high ambient temperatures with low initial capital investment.",
                "specs": {
                    "Compressor Style": "Industrial Reciprocating Compressor",
                    "Maintenance": "Extremely low maintenance cost with simple serviceable parts",
                    "Ambient Range": "Engineered to withstand extreme ambient temperatures",
                    "Durability": "Robust structural steel base frame"
                }
            },
            {
                "id": "bulk-milk-cooler",
                "name": "Bulk Milk Cooler (BMC)",
                "category": "dairy",
                "image": "assets/images/cold_store.png",
                "badge": "Dairy Special",
                "desc": "Direct expansion (DX) milk cooling tanks (open & closed styles) designed for quick thermal drop to preserve milk quality.",
                "specs": {
                    "Capacities": "Wide range from 500 liters to 5,000 liters",
                    "Tank Material": "Food-grade AISI-304 Stainless Steel with high-density insulation",
                    "Agitator": "Heavy-duty slow speed agitator with automatic cycle settings",
                    "Options": "Automatic CIP cleaning system, waste heat recovery coils"
                }
            },
            {
                "id": "cold-store",
                "name": "Prefabricated Cold Rooms",
                "category": "dairy",
                "image": "assets/images/cold_store.png",
                "badge": "High Density PUF",
                "desc": "Modular puff panel chambers assembled on-site with magnetic gaskets and digital control displays for temperature sensitive warehousing.",
                "specs": {
                    "Standard Temperature": "2°C to 4°C (Standard)",
                    "Extreme Temperature": "Deep freezing down to -18°C",
                    "Panels": "High-density PUF core wrapped in pre-painted G.I. sheet metal",
                    "Safety": "Door frame heaters for low temperature, emergency inner release handles"
                }
            },
            {
                "id": "air-washer",
                "name": "Air Washer & Pressurization",
                "category": "hvac",
                "image": "assets/images/hero.png",
                "badge": "Evaporative Cooling",
                "desc": "High-efficiency industrial evaporative air cooling units with cross-corrugated cellulose paper media and anti-vibration blowers.",
                "specs": {
                    "Cooling Pad": "Cross-corrugated cellulose paper pads with anti-algae treat",
                    "Structure": "Double skin panels in G.I. or pre-coated sheets",
                    "Blower Assembly": "Dynamically balanced blowers mounted on anti-vibration bases",
                    "Recommended For": "Hotels, large production floors, plastic extrusion units, canteens"
                }
            },
            {
                "id": "air-handling-unit",
                "name": "Air Handling Unit (AHU)",
                "category": "hvac",
                "image": "assets/images/hero.png",
                "badge": "Modular Design",
                "desc": "Double-skinned modular AHUs intended for general ventilation, air filtration, and centralized cooling layouts in commercial structures.",
                "specs": {
                    "Mounting Options": "Floor mounted, ceiling suspended, or loft installation",
                    "Filters": "Pre-filters (G.I. wiremesh) and fine synthetic media filters",
                    "Bearings": "Imported self-aligning pillow block bearings",
                    "Casing": "Aluminum profile frames with injected PUF panels"
                }
            },
            {
                "id": "ductable-ac",
                "name": "Ductable AC & Package Units",
                "category": "hvac",
                "image": "assets/images/hero.png",
                "badge": "5TR to 20TR",
                "desc": "High-static package and ductable central air conditioners for commercial retail spaces, offices, and industrial workspace cooling.",
                "specs": {
                    "Capacity Range": "5 TR to 20 TR models available",
                    "Mounting": "Floor-standing and ceiling-suspended options",
                    "Controls": "Digital programmable microprocessor based",
                    "Noise Levels": "Optimized scroll compressor with acoustic lining for low noise"
                }
            },
            {
                "id": "ducting-insulation",
                "name": "Ducting & Thermal Insulation",
                "category": "hvac",
                "image": "assets/images/hero.png",
                "badge": "SMACNA Standards",
                "desc": "Precision-fabricated galvanized iron (G.I.) and aluminum air distribution ducting with premium insulation wrap overlays.",
                "specs": {
                    "Material": "Galvanized steel sheets as per SMACNA parameters",
                    "Insulation": "Nitrile rubber or glass-wool insulation overlays",
                    "Aesthetics": "Perfect shape finishes with structural support hangers",
                    "Grilles & Diffusers": "Anodized aluminum supply and return air grilles"
                }
            },
            {
                "id": "electricals-electronics",
                "name": "Industrial Electrical Services",
                "category": "custom",
                "image": "assets/images/hero.png",
                "badge": "Turnkey Setup",
                "desc": "End-to-end design, cable routing, panel manufacturing, and site commissioning services for industrial electrical grids.",
                "specs": {
                    "Sectors Served": "Commercial, industrial, dairy, and agricultural projects",
                    "Scope": "Design, electrical load calculations, MCC panel fabrication, commissioning",
                    "Standard compliance": "Compliance with standard Indian Electricity (IE) rules",
                    "Team": "Certified electrical engineers and project managers"
                }
            }
        ]
        for prod in default_products:
            cursor.execute('''
                INSERT INTO products (id, name, category, image, badge, desc, specs)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (prod["id"], prod["name"], prod["category"], prod["image"], prod["badge"], prod["desc"], json.dumps(prod["specs"])))
        conn.commit()

    conn.close()

def add_inquiry(name, company, email, phone, city, product, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO inquiries (name, company, email, phone, city, product, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, company, email, phone, city, product, message, created_at))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id

def get_inquiries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inquiries ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_catalog_download(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO catalog_downloads (email, created_at)
        VALUES (?, ?)
    ''', (email, created_at))
    conn.commit()
    conn.close()

def get_catalog_downloads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM catalog_downloads ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_chat(user_message, bot_response):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO chats (user_message, bot_response, created_at)
        VALUES (?, ?, ?)
    ''', (user_message, bot_response, created_at))
    conn.commit()
    conn.close()

def get_chats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chats ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Product CRUD Helpers
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    products_list = []
    for r in rows:
        p = dict(r)
        try:
            p['specs'] = json.loads(p['specs'])
        except:
            p['specs'] = {}
        products_list.append(p)
    return products_list

def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        p = dict(row)
        try:
            p['specs'] = json.loads(p['specs'])
        except:
            p['specs'] = {}
        return p
    return None

def add_product(product_id, name, category, image, badge, desc, specs):
    conn = get_db_connection()
    cursor = conn.cursor()
    specs_str = json.dumps(specs) if isinstance(specs, (dict, list)) else specs
    cursor.execute('''
        INSERT INTO products (id, name, category, image, badge, desc, specs)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, name, category, image, badge, desc, specs_str))
    conn.commit()
    conn.close()

def update_product(product_id, name, category, image, badge, desc, specs):
    conn = get_db_connection()
    cursor = conn.cursor()
    specs_str = json.dumps(specs) if isinstance(specs, (dict, list)) else specs
    cursor.execute('''
        UPDATE products
        SET name = ?, category = ?, image = ?, badge = ?, desc = ?, specs = ?
        WHERE id = ?
    ''', (name, category, image, badge, desc, specs_str, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

