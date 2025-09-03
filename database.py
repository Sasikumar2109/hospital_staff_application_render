import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv
import file_utils
import json
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

DB_PATH = Path(__file__).parent / 'hospital_staff.db'
machine = os.getenv("MACHINE")
db_user = os.getenv("DB_USER")
db_pw = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

db_sslmode=os.getenv("SSL_MODE")
db_sslcert=os.getenv("SSL_CERT")
db_sslkey=os.getenv("SSL_KEY")
db_sslrootcert=os.getenv("SSL_ROOT_CERT")
db_instance_name = os.getenv("DB_INSTANCE_NAME")

if machine=='local':
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
else:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    import pg8000.native
    from google.cloud.sql.connector import Connector
    import sqlalchemy
    connector = Connector()

    def get_connection():
        conn = connector.connect(
            db_instance_name,  # e.g., hospital-app:us-central1:staff-db
            "pg8000",
            user=db_user,
            password=db_pw,
            db=db_name,
            ip_type = "PRIVATE"
        )
        return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            is_approved INTEGER DEFAULT 0,
            profile_status TEXT DEFAULT 'pending',
            designation TEXT,
            address TEXT,
            aadhaar TEXT,
            workplace TEXT,
            rnrm_doc_path TEXT,
            rnrm_number TEXT,
            emergency_contact TEXT,
            college TEXT,
            photo_path TEXT,
            aadhaar_doc_path TEXT,
            educational_qualification TEXT,
            blood_group TEXT,
            gender TEXT,
            member_id TEXT UNIQUE,
            signature_path TEXT,
            profile_submission_date TEXT,
            profile_approved_date TEXT,
            approved_by TEXT,
            UNIQUE(email, is_admin)
        )
    ''')
    # OTP table
    c.execute('''
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            purpose TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Association Info table
    c.execute('''
        CREATE TABLE IF NOT EXISTS association_info (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            association_name TEXT NOT NULL,
            association_register_number TEXT,
            primary_contact TEXT NOT NULL,
            secondary_contact TEXT,
            address TEXT NOT NULL,
            email TEXT,
            terms_file_path TEXT,
            last_update_by TEXT,
            last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_association_info():
    conn = get_connection()
    
    c = conn.cursor()

    c.execute('SELECT * FROM association_info WHERE id = 1')
    row = c.fetchall() #changes
    rows = file_utils.convert_to_dict(c,row)
    row = rows[0] if rows else None
    conn.close()
    return row

def update_association_info(association_name, association_register_number, primary_contact, secondary_contact, address, email, terms_file_path, last_update_by):
    conn = get_connection()
    if machine=='local':
        c = conn.cursor()
    else:
        c = conn.cursor()    # Use India timezone for last_updated_at
    try:
        from zoneinfo import ZoneInfo
        import datetime
        now_str = datetime.datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    except ImportError:
        import pytz
        import datetime
        now_str = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    query = '''
        INSERT INTO association_info (id, association_name, association_register_number, primary_contact, secondary_contact, address, email, terms_file_path, last_update_by, last_updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            association_name=excluded.association_name,
            association_register_number=excluded.association_register_number,
            primary_contact=excluded.primary_contact,
            secondary_contact=excluded.secondary_contact,
            address=excluded.address,
            email=excluded.email,
            terms_file_path=excluded.terms_file_path,
            last_update_by=excluded.last_update_by,
            last_updated_at=excluded.last_updated_at
    '''
    params = (association_name, association_register_number, primary_contact, secondary_contact, address, email, terms_file_path, last_update_by, now_str)

    file_utils.execute_query(cursor=c,query=query,params=params,machine=machine)
        
    conn.commit()
    conn.close()

# if __name__ == '__main__':
#     init_db()