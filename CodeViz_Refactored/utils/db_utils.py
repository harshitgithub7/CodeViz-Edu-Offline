import sqlite3
import os

def get_connection(db_path="db/content.db"):
    abs_path = os.path.abspath(db_path)
    return sqlite3.connect(abs_path)


def fetch_concepts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic, content FROM concepts")
    data = cursor.fetchall()
    conn.close()
    return data