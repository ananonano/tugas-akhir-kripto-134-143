# Nama file: pages/3_Sisipkan_Data_PVD.py
import streamlit as st
from crypto_modules import pvd_hide_message, pvd_reveal_message
# --- PERBAIKAN IMPORT ---
from database import add_history_entry, get_user_history
from PIL import Image
import io
import json

st.set_page_config(page_title="Sisipkan Data PVD", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Penyisipan Data Gambar (PVD)")
st.caption("Menyisipkan data rahasia (watermark/ID transaksi) ke dalam gambar (misal: bukti transfer).")
user_id = st.session_state['user_id']

# --- FUNGSI HELPER DIDEFINISIKAN DI SINI ---
def get_transaction_options(user_id):
    all_history = get_user_history(user_id)
    transaction_logs = [entry for entry in all_history if entry['action'] == "Catat Transaksi"]
    
    options = {"Tidak terkait transaksi": None}
    
    for entry in transaction_logs:
        try:
            data = json.loads(entry['details'])
            tx_id = entry['id'] # <-- Membaca ID dari history
            display_str = f"{entry['timestamp'].strftime('%Y-%m-%d %H:%M')} - {data.get('keterangan', 'N/A')} (Rp {data.get('nominal', 0):,.0f})"
            options[display_str] = tx_id
        except (json.JSONDecodeError, TypeError, KeyError):
            pass # Lewati log yang rusak atau tidak punya 'id'
            
    return options

# Panggil fungsi yang ada di file ini
tx_options = get_transaction_options(user_id)

tab1, tab2 = st.tabs(["Sisipkan Data", "Ekstrak Data"])

with tab1:
    st.header("Sisipkan Data Rahasia")
    
    selected_tx_display = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(),
        key="tx_e_pvd"
    )
    selected_tx_id = tx_options[selected_tx_display]
    
    cover_image = st.file_uploader("Upload Gambar Cover (.png):", type=['png'], key="pvd_cover")
    secret_message = st.text_area("Data Rahasia (misal: ID Transaksi):", key="pvd_msg")
    
    if st.button("Sisipkan"):
        if cover_image and secret_message:
            try:
                img = Image.open(cover_image)
                stego_img = pvd_hide_message(img, secret_message) 
                
                st.subheader("Gambar Stego Berhasil Dibuat:")
                st.image(stego_img, caption="Gambar dengan data tersembunyi")
                
                buf = io.BytesIO()
                stego_img.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                
                st.download_button(
                    label="Download Gambar Stego",
                    data=img_bytes,
                    file_name="stego_image_pvd.png",
                    mime="image/png"
                )
                
                log_data = {
                    "file_name": cover_image.name,
                    "message_hint": secret_message[:20] + "...",
                    "linked_tx_id": selected_tx_id
                }
                add_history_entry(user_id, "PVD Hide", json.dumps(log_data))
                
            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Harap upload gambar cover dan masukkan data rahasia.")

with tab2:
    st.header("Ekstrak Data Rahasia")
    
    selected_tx_display_d = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(),
        key="tx_d_pvd"
    )
    selected_tx_id_d = tx_options[selected_tx_display_d]
    
    stego_image_file = st.file_uploader("Upload Gambar Stego (.png):", type=['png'], key="pvd_stego")
    
    if st.button("Ekstrak"):
        if stego_image_file:
            try:
                img = Image.open(stego_image_file)
                revealed_message = pvd_reveal_message(img) 
                
                if revealed_message is not None:
                    st.subheader("Data yang Ditemukan:")
                    st.text_area("Data:", value=revealed_message, height=150, disabled=True)
                    
                    log_data = {
                        "file_name": stego_image_file.name,
                        "revealed_hint": revealed_message[:20] + "...",
                        "linked_tx_id": selected_tx_id_d
                    }
                    add_history_entry(user_id, "PVD Reveal", json.dumps(log_data))
                else:
                    st.error("Tidak ada data tersembunyi yang ditemukan (gambar ini mungkin bukan stego PVD).")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        else:
            st.warning("Harap upload gambar stego.")
            
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()