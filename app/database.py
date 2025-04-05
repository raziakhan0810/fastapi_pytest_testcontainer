import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from typing import List, Dict

# Database connection setup
DATABASE_URL = "postgresql://testuser:testpassword@localhost/testdb"

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def create_user(username: str, email: str, password: str) -> Dict:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create a user in the PostgreSQL database
            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s) RETURNING id, username, email
            """, (username, email, password))
            conn.commit()
            user = cur.fetchone()
            return {"id": user[0], "username": user[1], "email": user[2]}

def get_users(limit: int = 100, offset: int = 0) -> List[Dict]:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email FROM users
                LIMIT %s OFFSET %s
            """, (limit, offset))
            users = cur.fetchall()
            return [{"id": user[0], "username": user[1], "email": user[2]} for user in users]

def get_user_by_id(user_id: int) -> Dict:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email FROM users WHERE id = %s
            """, (user_id,))
            user = cur.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            return None
