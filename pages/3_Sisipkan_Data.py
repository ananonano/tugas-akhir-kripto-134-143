import streamlit as st
from crypto_modules import lsb_rc4_hide, lsb_rc4_reveal
from database import add_history_entry, get_user_history
from PIL import Image
import io
import json

st.set_page_config(page_title="Sisipkan Data LSB", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Penyisipan Data Gambar (LSB + RC4)")
st.caption("Menyisipkan data rahasia terenkripsi (watermark/ID) ke dalam gambar (misal: bukti transfer).")
user_id = st.session_state['user_id']

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

tab1, tab2 = st.tabs(["Sisipkan Data", "Ekstrak Data"])

with tab1:
    st.header("Sisipkan Data Rahasia (LSB-RC4 Hide)")
    
    selected_tx_display = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(),
        key="tx_e_lsb"
    )
    selected_tx_id = tx_options[selected_tx_display]
    
    cover_image = st.file_uploader("Upload Gambar Cover (.png):", type=['png'], key="lsb_cover")
    secret_message = st.text_area("Data Rahasia (misal: ID Transaksi):", key="lsb_msg")
    
    rc4_key_e = st.text_input("Kunci RC4:", key="lsb_key_e", type="password")
    
    if st.button("Sisipkan"):
        if cover_image and secret_message and rc4_key_e:
            try:
                img = Image.open(cover_image)
                stego_img = lsb_rc4_hide(img, secret_message, rc4_key_e) 
                
                st.subheader("Gambar Stego Berhasil Dibuat:")
                st.image(stego_img, caption="Gambar dengan data tersembunyi")
                
                buf = io.BytesIO()
                stego_img.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                
                st.download_button(
                    label="Download Gambar Stego",
                    data=img_bytes,
                    file_name="stego_image_lsb_rc4.png",
                    mime="image/png"
                )
                
                key_hint = rc4_key_e[:2] + "..." + rc4_key_e[-2:] if len(rc4_key_e) > 4 else rc4_key_e
                log_data = {
                    "file_name": cover_image.name,
                    "message_hint": secret_message[:20] + "...",
                    "key_hint": key_hint,
                    "linked_tx_id": selected_tx_id
                }
                add_history_entry(user_id, "LSB-RC4 Hide", json.dumps(log_data))
                
            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Harap upload gambar cover, masukkan data rahasia, dan masukkan Kunci RC4.")

with tab2:
    st.header("Ekstrak Data Rahasia (LSB-RC4 Reveal)")
    
    selected_tx_display_d = st.selectbox(
        "Tautkan ke Transaksi (Opsional):", 
        options=tx_options.keys(),
        key="tx_d_lsb"
    )
    selected_tx_id_d = tx_options[selected_tx_display_d]
    
    stego_image_file = st.file_uploader("Upload Gambar Stego (.png):", type=['png'], key="lsb_stego")
    
    #TAMBAHAN INPUT KUNCI
    rc4_key_d = st.text_input("Kunci RC4:", key="lsb_key_d", type="password")

    if st.button("Ekstrak"):
        if stego_image_file and rc4_key_d:
            try:
                img = Image.open(stego_image_file)
                revealed_message = lsb_rc4_reveal(img, rc4_key_d) 
                
                if revealed_message is not None:
                    st.subheader("Data yang Ditemukan:")
                    st.text_area("Data:", value=revealed_message, height=150, disabled=True)
                    
                    log_data = {
                        "file_name": stego_image_file.name,
                        "revealed_hint": revealed_message[:20] + "...",
                        "linked_tx_id": selected_tx_id_d
                    }
                    add_history_entry(user_id, "LSB-RC4 Reveal", json.dumps(log_data))
                else:
                    st.error("Tidak ada data tersembunyi yang ditemukan (gambar ini mungkin bukan stego LSB atau kunci RC4 salah).")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        else:
            st.warning("Harap upload gambar stego dan masukkan Kunci RC4.")
            
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()