import psycopg2
import os
from fastapi import HTTPException
from app.database.connection import get_connection
from app.models.user import LoginAccount

# TESTING PURPOSE
def drop_passwords_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE passwords CASCADE;")
    print("Deleted table")
    conn.commit()
    cursor.close()
    conn.close()
    
def print_passwords_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM passwords;")
    rows = cursor.fetchall()

    print("\n--- PASSWORDS TABLE DATA ---")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
# MAIN AUTH TABLE

def create_table_users():
    conn = get_connection()
    cursor = conn.cursor()
    # Creates table with the columns - ID,email,hashed_password,created_at
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users(
                       id UUID PRIMARY KEY,
                       email TEXT UNIQUE,
                       hashed_password TEXT,
                       created_at TEXT
                   )
                   """)
    conn.commit()
    cursor.close()
    conn.close()

def create_table_passwords():
    conn = get_connection()
    cursor = conn.cursor()
    # Creates table with the columns - ID,user_ID,site,email,hashed_password,data_entry
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS passwords(
                       id UUID PRIMARY KEY,
                       user_id UUID REFERENCES users(id),
                       site_link TEXT,
                       username TEXT,
                       email TEXT,
                       hashed_password TEXT,
                       date_entry TEXT
                   )
                   """)
    print("created")
    conn.commit()
    cursor.close()
    conn.close()


# REGISTER FUNCTIONS

def insert_account(id,email,hashed_password,created_at):
    conn = get_connection()
    cursor = conn.cursor()
    # Insert data into user table
    cursor.execute("""
                   INSERT INTO users
                   VALUES (%s,%s,%s,%s)
                   """,(id,email,hashed_password,created_at)) 
    conn.commit()
    cursor.close()
    conn.close()
def insert_userpassword(password_id,user_id,site_link,email,hashed_password,date_entry):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO passwords
                   VALUES (%s,%s,%s,%s,%s,%s)
                   """,(password_id,user_id,site_link,email,hashed_password,date_entry))
    conn.commit()
    cursor.close()
    conn.close()

# LOGIN FUNCTIONS

def account_check(email:str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM users WHERE email = %s
                   """,(email,))
    user = cursor.fetchone()
    return user


# MAIN PASSWORD MANAGER

def insert_data(password_id,user_id,site_link,username,email,password,date_entry):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO passwords(id,user_id,site_link,username,email,hashed_password,date_entry)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """,(password_id,user_id,site_link,username,email,password,date_entry))
    conn.commit()
    cursor.close()
    conn.close()

def account_check(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM users WHERE email = %s
                   """,(email,))
    user = cursor.fetchone()
    return user

def account_check_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM users WHERE id = %s
                   """,(user_id,))
    user = cursor.fetchone()
    return user

def get_passwords_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM passwords WHERE user_id = %s
        """, (user_id,))
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        conn.close()


def get_password_records(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM passwords WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchall()