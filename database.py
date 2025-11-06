import streamlit as st
import mysql.connector # Kita masih butuh ini untuk 'Error'
import datetime
from crypto_modules import des_encrypt, des_decrypt
import pandas as pd
from sqlalchemy import text # Pastikan ini ada

# Kunci DES tetap di sini
DB_HISTORY_KEY = b'MySecret' 

@st.cache_resource
def get_db_connection():
    """Membuat koneksi baru menggunakan st.connection."""
    try:
        conn = st.connection("mysql_db", type="sql")
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def init_db():
    """Membuat tabel database jika belum ada."""
    conn = get_db_connection()
    if conn is None:
        st.error("Could not connect to database for initialization.", icon="🚨")
        return

    try:
        with conn.session as s:
            s.execute(text('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
            '''))
            s.execute(text('''
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                timestamp DATETIME NOT NULL,
                action_type VARCHAR(255) NOT NULL,
                encrypted_log_entry BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            '''))
            s.commit()
    except (mysql.connector.Error, Exception) as e:
        st.error(f"Error creating tables: {e}", icon="🚨")

def add_user_to_db(username, password_hash):
    """Menambahkan user baru ke database."""
    conn = get_db_connection()
    if conn is None: return False
    
    try:
        with conn.session as s:
            query = "INSERT INTO users (username, password_hash) VALUES (:username, :pass_hash)"
            s.execute(text(query), params={"username": username, "pass_hash": password_hash})
            s.commit()
        return True
    except mysql.connector.Error as e:
        if e.errno == 1062:
             st.error(f"Gagal mendaftar: Username '{username}' sudah digunakan.", icon="🚫")
        else:
             st.error(f"Error adding user: {e}", icon="🚨")
        return False

def get_user_from_db(username):
    """Mengambil data user berdasarkan username."""
    conn = get_db_connection()
    if conn is None: return None
    
    try:
        query = "SELECT * FROM users WHERE username = :username"
        df = conn.query(query, params={"username": username}, ttl=0)
        
        if df.empty:
            return None
        else:
            user_data = tuple(df.iloc[0])
            user_data = (int(user_data[0]), user_data[1], user_data[2]) # Fix int64
            return user_data
            
    except mysql.connector.Error as e:
        st.error(f"Error getting user: {e}", icon="🚨")
        return None

def add_history_entry(user_id, action_type, log_details):
    """Menambahkan entri history, dienkripsi dengan DES."""
    conn = get_db_connection()
    if conn is None: return False
    
    try:
        timestamp = datetime.datetime.now()
        encrypted_log = des_encrypt(log_details.encode('utf-8'), DB_HISTORY_KEY)

        with conn.session as s:
            query = """
            INSERT INTO history (user_id, timestamp, action_type, encrypted_log_entry) 
            VALUES (:uid, :ts, :action, :log)
            """
            s.execute(text(query), params={
                "uid": user_id, 
                "ts": timestamp, 
                "action": action_type, 
                "log": encrypted_log
            })
            s.commit()
        return True
    except (mysql.connector.Error, Exception) as e:
        st.error(f"Error adding history: {e}", icon="🚨")
        return False

# ==========================================================
# INI FUNGSI YANG UDAH DIBENERIN (FIX KEYERROR: 'id')
# ==========================================================
def get_user_history(user_id):
    """Mengambil dan mendekripsi history untuk user tertentu."""
    conn = get_db_connection()
    if conn is None: return []

    history_list = []
    try:
        # 1. PERBAIKAN: Tambahkan 'id' di SELECT
        query = "SELECT id, timestamp, action_type, encrypted_log_entry FROM history WHERE user_id = :uid ORDER BY timestamp DESC"
        df = conn.query(query, params={"uid": user_id}, ttl=0) 

        # Loop DataFrame-nya
        for row in df.itertuples(index=False):
            # 2. PERBAIKAN: Ambil 'id' dari row
            id, timestamp, action_type, encrypted_log = row
            
            try:
                decrypted_log = des_decrypt(encrypted_log, DB_HISTORY_KEY).decode('utf-8')
                
                # 3. PERBAIKAN: Masukkan 'id' ke dictionary
                history_list.append({
                    "id": id, # <-- INI DIA
                    "timestamp": timestamp,
                    "action": action_type,
                    "details": decrypted_log
                })
            except Exception as e:
                history_list.append({
                    "id": id, # <-- INI DIA
                    "timestamp": timestamp,
                    "action": action_type,
                    "details": f"[Error dekripsi log: {e}]"
                })
                
    except mysql.connector.Error as e:
        st.error(f"Error getting history: {e}")
        
    return history_list