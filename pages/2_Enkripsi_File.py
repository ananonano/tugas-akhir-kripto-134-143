import streamlit as st
from crypto_modules import cast_encrypt_file, cast_decrypt_file
from database import add_history_entry

st.set_page_config(page_title="Enkripsi File", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title("Enkripsi File (CAST-128)")
user_id = st.session_state['user_id']

tab1, tab2 = st.tabs(["Enkripsi File", "Dekripsi File"])

with tab1:
    st.header("Enkripsi File")
    uploaded_file_e = st.file_uploader("Upload file untuk dienkripsi:", key="tf_file_e")
    tf_key_e = st.text_input("Kunci CAST-128 (16 bytes):", key="tf_key_e").encode('utf-8')
    
    if st.button("Enkripsi File"):
        if uploaded_file_e and tf_key_e and len(tf_key_e) == 16:
            file_bytes = uploaded_file_e.getvalue()
            encrypted_file = cast_encrypt_file(file_bytes, tf_key_e)
            
            st.success("File berhasil dienkripsi!")
            st.download_button(
                label="Download File Terenkripsi",
                data=encrypted_file,
                file_name=f"{uploaded_file_e.name}.enc",
                mime="application/octet-stream"
            )
            # Simpan history
            log = f"File: '{uploaded_file_e.name}' | Key: '{tf_key_e.decode()}'"
            add_history_entry(user_id, "CAST-128 Enkripsi File", log)
        else:
            st.warning("Upload file dan masukkan kunci CAST-128 yang valid (tepat 16 byte).")

with tab2:
    st.header("Dekripsi File")
    uploaded_file_d = st.file_uploader("Upload file untuk didekripsi (.enc):", key="tf_file_d")
    tf_key_d = st.text_input("Kunci CAST-128 (16 bytes):", key="tf_key_d").encode('utf-8')

    if st.button("Dekripsi File"):
        if uploaded_file_d and tf_key_d and len(tf_key_d) == 16:
            file_bytes = uploaded_file_d.getvalue()
            decrypted_file = cast_decrypt_file(file_bytes, tf_key_d)
            
            if decrypted_file:
                st.success("File berhasil didekripsi!")
                out_name = uploaded_file_d.name.replace(".enc", "") if ".enc" in uploaded_file_d.name else f"decrypted_{uploaded_file_d.name}" # Mengambil nama asli (menghapus .enc jika ada)
                
                st.download_button(
                    label="Download File Terdekripsi",
                    data=decrypted_file,
                    file_name=out_name,
                    mime="application/octet-stream"
                )
                # Simpan history
                log = f"File: '{uploaded_file_d.name}' | Key: '{tf_key_d.decode()}'"
                add_history_entry(user_id, "CAST-128 Dekripsi File", log)
            else:
                st.error("Gagal mendekripsi file. Kunci salah atau file korup.")
        else:
            st.warning("Upload file dan masukkan kunci CAST-128 yang valid (tepat 16 byte).")
            

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()