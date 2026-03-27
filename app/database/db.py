import psycopg2
import os
from fastapi import HTTPException
from app.database.connection import get_connection
from app.models.user import LoginAccount

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
                       site TEXT,
                       email TEXT UNIQUE,
                       hashed_password TEXT,
                       date_entry TEXT
                   )
                   """)
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
def insert_userpassword(id,user_id,site,email,hashed_password,data_entry):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO passwords
                   VALUES (%s,%s,%s,%s,%s,%s)
                   """,(id,user_id,site,email,hashed_password,data_entry))
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


def password_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS passwords(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id TEXT NOT NULL,
                   site_link TEXT NOT NULL,
                   username TEXT,
                   email TEXT,
                   encrypted_password TEXT NOT NULL,
                   created_at TEXT
                   )
                   """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(user_id,site_link,username,email,password):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT * INTO passwords(user_id,site_link,username,email,password)
                   """,user_id,site_link,username,email,password)
    conn.commit()
    cursor.close()
    conn.close()