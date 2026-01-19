import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = 'postgres'
DB_USER = 'postgres.fzhueoayckxgcswuaxcy'
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = 'aws-1-us-east-1.pooler.supabase.com'
DB_PORT = '6543'

print(f"Connecting to {DB_HOST}...")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        sslmode='require'
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    if not DB_PASS:
        print("⚠️  Warning: DB_PASSWORD environment variable is empty or not set.")
