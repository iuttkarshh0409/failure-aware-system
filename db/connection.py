import sqlite3
import os

DB_PATH = "db/failure_aware.db"

def get_connection():
    os.makedirs("db", exist_ok=True)
    print("DB PATH:", DB_PATH)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

