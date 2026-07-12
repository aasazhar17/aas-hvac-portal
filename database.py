import sqlite3
import os
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
