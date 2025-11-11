import streamlit as st
from crypto_modules import cast_encrypt_file, cast_decrypt_file 
from database import add_history_entry, get_user_history 
import json

st.set_page_config(page_title="Enkripsi Struk", layout="wide")

# 1. PENGECEKAN SESI LOGIN
if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Enkripsi Struk / Bukti Transfer (CAST-128)")
user_id = st.session_state['user_id']

# 2. FUNGSI HELPER UNTUK SELECTBOX 
def get_transaction_options(user_id):
    all_history = get_user_history(user_id) 
    transaction_logs = [entry for entry in all_history if entry['action'] == "Catat Transaksi"]
    
    options = {"Tidak terkait transaksi": None}
    
    for entry in transaction_logs:
        try:
            data = json.loads(entry['details'])
            tx_id = entry['id'] 
            display_str = f"{entry['timestamp'].strftime('%Y-%m-%d %H:%M')} - {data.get('keterangan', 'N/A')} (Rp {data.get('nominal', 0):,.0f})"
            options[display_str] = tx_id
        except (json.JSONDecodeError, TypeError, KeyError):
            pass 
            
    return options 

tx_options = get_transaction_options(user_id)

# 3. PEMBUATAN TABS 
tab1, tab2 = st.tabs(["Enkripsi Struk", "Dekripsi Struk"])

# TAB 1: ENKRIPSI STRUK 
with tab1:
    st.header("Enkripsi File Struk (JPG, PNG, PDF, dll)")
    
    selected_tx_display = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(), 
        key="tx_e" 
    )
    selected_tx_id = tx_options[selected_tx_display] 
    
    uploaded_file_e = st.file_uploader("Upload Struk/Bukti untuk dienkripsi:", key="tf_file_e")
    tf_key_e = st.text_input("Kunci CAST-128 (16 bytes):", key="tf_key_e").encode('utf-8')
    
    if st.button("Enkripsi File"):
        if uploaded_file_e and tf_key_e and len(tf_key_e) == 16:
            file_bytes = uploaded_file_e.getvalue()
            encrypted_file = cast_encrypt_file(file_bytes, tf_key_e)
            
            st.success("Struk berhasil dienkripsi!")
            st.download_button(
                label="Download Struk Terenkripsi",
                data=encrypted_file,
                file_name=f"{uploaded_file_e.name}.enc", 
                mime="application/octet-stream" 
            )
            
            # Siapkan data log (dalam format JSON)
            log_data = {
                "file_name": uploaded_file_e.name,
                "key_hint": tf_key_e.decode()[:3] + "..." + tf_key_e.decode()[-3:], # Petunjuk kunci (3 depan, 3 belakang)
                "linked_tx_id": selected_tx_id # ID transaksi yang ditautkan (bisa None)
            }
            # Simpan log aktivitas ke database (akan dienkripsi DES)
            add_history_entry(user_id, "CAST-128 Enkripsi Struk", json.dumps(log_data))
        else:
            st.warning("Upload file struk dan masukkan kunci CAST-128 yang valid (tepat 16 byte).")

# TAB 2: DEKRIPSI STRUK 
with tab2:
    st.header("Dekripsi File Struk")
    
    selected_tx_display_d = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(),
        key="tx_d"
    )
    selected_tx_id_d = tx_options[selected_tx_display_d]
    
    uploaded_file_d = st.file_uploader("Upload Struk terenkripsi (.enc):", key="tf_file_d")
    tf_key_d = st.text_input("Kunci CAST-128 (16 bytes):", key="tf_key_d").encode('utf-8')

    if st.button("Dekripsi File"):
        if uploaded_file_d and tf_key_d and len(tf_key_d) == 16:
            file_bytes = uploaded_file_d.getvalue()
            decrypted_file = cast_decrypt_file(file_bytes, tf_key_d)
            
            if decrypted_file:
                st.success("Struk berhasil didekripsi!")
                out_name = uploaded_file_d.name.replace(".enc", "") if ".enc" in uploaded_file_d.name else f"decrypted_{uploaded_file_d.name}"
                
                st.download_button(
                    label="Download Struk Asli",
                    data=decrypted_file,
                    file_name=out_name,
                    mime="application/octet-stream"
                )
                
                log_data = {
                    "file_name": uploaded_file_d.name,
                    "linked_tx_id": selected_tx_id_d
                }
                add_history_entry(user_id, "CAST-128 Dekripsi Struk", json.dumps(log_data))
            else:
                st.error("Gagal mendekripsi struk. Kunci salah atau file korup.")
        else:
            st.warning("Upload file struk dan masukkan kunci CAST-128 yang valid (tepat 16 byte).")
            
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['user_id'] = 0
    st.rerun()