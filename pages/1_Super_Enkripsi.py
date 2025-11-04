import streamlit as st
from crypto_modules import super_encrypt, super_decrypt
from database import add_history_entry
import base64

st.set_page_config(page_title="Super Enkripsi", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Super Enkripsi (Vigenere + Blowfish)")
user_id = st.session_state['user_id']

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    st.header("Enkripsi Teks")
    plain_text = st.text_area("Masukkan Teks di sini:", key="se_plain")
    v_key = st.text_input("Kunci Vigenere (hanya huruf):", key="se_vkey_e").upper()
    b_key = st.text_input("Kunci Blowfish (min 8 byte):", key="se_bkey_e").encode('utf-8')
    
    if st.button("Enkripsi"):
        if plain_text and v_key.isalpha() and len(b_key) >= 8:
            try:
                encrypted_data = super_encrypt(plain_text, v_key, b_key)
                encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
                st.subheader("Hasil Enkripsi (Base64):")
                st.code(encrypted_text, language=None)
                
                # Simpan history
                log = f"Plain: '{plain_text[:20]}...' | V-Key: '{v_key}' | B-Key: '{b_key.decode()}'"
                add_history_entry(user_id, "Super Enkripsi", log)
                
            except Exception as e:
                st.error(f"Error: {e}. Pastikan kunci Blowfish valid (8-56 bytes).")
        else:
            st.warning("Pastikan semua field diisi. Kunci Vigenere harus huruf, Kunci Blowfish min 8 byte.")

with tab2:
    st.header("Dekripsi Teks")
    cipher_text_b64 = st.text_area("Masukkan Teks (Base64) di sini:", key="se_cipher")
    v_key_d = st.text_input("Kunci Vigenere (hanya huruf):", key="se_vkey_d").upper()
    b_key_d = st.text_input("Kunci Blowfish (min 8 byte):", key="se_bkey_d").encode('utf-8')

    if st.button("Dekripsi"):
        if cipher_text_b64 and v_key_d.isalpha() and len(b_key_d) >= 8:
            try:
                cipher_data = base64.b64decode(cipher_text_b64)
                decrypted_text = super_decrypt(cipher_data, v_key_d, b_key_d)
                
                st.subheader("Hasil Dekripsi:")
                st.text(decrypted_text)
                
                # Simpan history
                log = f"Cipher: '{cipher_text_b64[:20]}...' | V-Key: '{v_key_d}' | B-Key: '{b_key_d.decode()}'"
                add_history_entry(user_id, "Super Dekripsi", log)
                
            except Exception as e:
                st.error(f"Error dekripsi: {e}. Pastikan kunci dan data Base64 benar.")
        else:
            st.warning("Pastikan semua field diisi. Kunci Vigenere harus huruf, Kunci Blowfish min 8 byte.")
            
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()