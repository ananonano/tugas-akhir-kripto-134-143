import streamlit as st
from crypto_modules import lsb_hide_message, lsb_reveal_message
from database import add_history_entry
from PIL import Image
import io

st.set_page_config(page_title="Steganografi LSB", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Steganografi Gambar (LSB)")
user_id = st.session_state['user_id']

tab1, tab2 = st.tabs(["Sembunyikan Pesan", "Ungkap Pesan"])

with tab1:
    st.header("Sembunyikan Pesan")
    cover_image = st.file_uploader("Upload Gambar Cover (.png):", type=['png'], key="lsb_cover")
    secret_message = st.text_area("Pesan Rahasia:", key="lsb_msg")
    
    if st.button("Sembunyikan"):
        if cover_image and secret_message:
            try:
                img = Image.open(cover_image)
                stego_img = lsb_hide_message(img, secret_message)
                
                st.subheader("Gambar Stego Berhasil Dibuat:")
                st.image(stego_img, caption="Gambar dengan pesan tersembunyi")
                
                # Konversi PIL Image ke bytes untuk download
                buf = io.BytesIO()
                stego_img.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                
                st.download_button(
                    label="Download Gambar Stego",
                    data=img_bytes,
                    file_name="stego_image.png",
                    mime="image/png"
                )
                
                # Simpan history
                log = f"Cover Image: '{cover_image.name}' | Pesan: '{secret_message[:20]}...'"
                add_history_entry(user_id, "LSB Hide", log)
                
            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Harap upload gambar cover dan masukkan pesan rahasia.")

with tab2:
    st.header("Ungkap Pesan")
    stego_image_file = st.file_uploader("Upload Gambar Stego (.png):", type=['png'], key="lsb_stego")
    
    if st.button("Ungkap"):
        if stego_image_file:
            try:
                img = Image.open(stego_image_file)
                revealed_message = lsb_reveal_message(img)
                
                if revealed_message is not None:
                    st.subheader("Pesan yang Ditemukan:")
                    st.text_area("Pesan:", value=revealed_message, height=150, disabled=True)
                    # Simpan history
                    log = f"Stego Image: '{stego_image_file.name}'"
                    add_history_entry(user_id, "LSB Reveal", log)
                else:
                    st.error("Tidak ada pesan tersembunyi yang ditemukan (atau delimiter tidak ada).")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        else:
            st.warning("Harap upload gambar stego.")
            
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()