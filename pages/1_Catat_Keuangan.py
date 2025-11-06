# Nama file: pages/1_Catat_Transaksi.py
import streamlit as st
from crypto_modules import super_encrypt, super_decrypt
from database import add_history_entry
import base64
import json

st.set_page_config(page_title="Catat Transaksi", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Catat Transaksi Keuangan (Super Enkripsi)")
st.caption("Data transaksi Anda akan dienkripsi berlapis (Vigenere + Blowfish) sebelum disimpan.")
user_id = st.session_state['user_id']

tab1, tab2 = st.tabs(["Catat Transaksi (Enkripsi)", "Lihat Transaksi (Dekripsi)"])

with tab1:
    st.header("Formulir Transaksi Baru")
    
    tipe_transaksi = st.selectbox("Tipe Transaksi", ["Pemasukan", "Pengeluaran"])
    nominal = st.number_input("Nominal (Rp)", min_value=0.0, step=1000.0)
    keterangan = st.text_input("Keterangan Singkat")
    
    st.divider()
    st.subheader("Kunci Keamanan")
    v_key = st.text_input("Kunci Vigenere (hanya huruf):", key="se_vkey_e").upper()
    b_key = st.text_input("Kunci Blowfish (min 8 byte):", key="se_bkey_e").encode('utf-8')
    
    if st.button("Simpan dan Enkripsi Transaksi"):
        if keterangan and v_key.isalpha() and len(b_key) >= 8 and nominal > 0:
            try:
                # 1. Gabungkan data terstruktur menjadi JSON string
                data = {
                    "tipe": tipe_transaksi,
                    "nominal": nominal,
                    "keterangan": keterangan
                }
                plain_text = json.dumps(data)
                
                # 2. Enkripsi data JSON tersebut
                encrypted_data = super_encrypt(plain_text, v_key, b_key)
                encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
                
                st.subheader("Data Transaksi Terenkripsi (Base64):")
                st.code(encrypted_text, language=None)
                st.success("Data transaksi berhasil dienkripsi!")
                
                # 3. Simpan log untuk audit (ini yang akan dibaca di halaman Laporan)
                # Kita simpan data MENTAH (sebelum super-enkripsi) ke log
                # Log ini akan dienkripsi oleh DES secara otomatis oleh add_history_entry
                log_data_json_string = json.dumps(data)
                add_history_entry(user_id, "Catat Transaksi", log_data_json_string)
                
            except Exception as e:
                st.error(f"Error: {e}. Pastikan kunci Blowfish valid (8-56 bytes).")
        else:
            st.warning("Pastikan semua field (Tipe, Nominal, Keterangan, Kunci V/B) diisi dengan benar.")

with tab2:
    st.header("Lihat Transaksi (Dekripsi)")
    cipher_text_b64 = st.text_area("Masukkan Data Transaksi (Base64) di sini:", key="se_cipher")
    
    st.divider()
    st.subheader("Kunci Keamanan")
    v_key_d = st.text_input("Kunci Vigenere (hanya huruf):", key="se_vkey_d").upper()
    b_key_d = st.text_input("Kunci Blowfish (min 8 byte):", key="se_bkey_d").encode('utf-8')

    if st.button("Dekripsi Transaksi"):
        if cipher_text_b64 and v_key_d.isalpha() and len(b_key_d) >= 8:
            try:
                cipher_data = base64.b64decode(cipher_text_b64)
                decrypted_text = super_decrypt(cipher_data, v_key_d, b_key_d)
                
                st.subheader("Hasil Dekripsi Transaksi:")
                
                # Coba parse JSON, jika gagal, tampilkan teks biasa (untuk data lama)
                try:
                    data = json.loads(decrypted_text)
                    st.json(data)
                except json.JSONDecodeError:
                    st.text(decrypted_text)
                
                # Simpan history
                log = f"Mendekripsi data: '{cipher_text_b64[:20]}...'"
                add_history_entry(user_id, "Dekripsi Transaksi", log)
                
            except Exception as e:
                st.error(f"Error dekripsi: {e}. Pastikan kunci dan data Base64 benar.")
        else:
            st.warning("Pastikan semua field (Data, Kunci V/B) diisi dengan benar.")
            
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()