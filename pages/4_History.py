import streamlit as st
from database import get_user_history
import pandas as pd

st.set_page_config(page_title="History", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title(f"History Aktivitas {st.session_state['username']}")

user_id = st.session_state['user_id']
history_data = get_user_history(user_id)

if not history_data:
    st.info("Anda belum memiliki riwayat aktivitas.")
else:
    st.write(f"Menampilkan **{len(history_data)}** riwayat terakhir:")
    
    for i, entry in enumerate(history_data):
        with st.expander(f"**{entry['timestamp']}** - **{entry['action']}**"):
            st.text(f"Detail:\n{entry['details']}")

    if st.checkbox("Tampilkan sebagai tabel (data mentah)"): # Opsi untuk menampilkan sebagai tabel
        df = pd.DataFrame(history_data)
        st.dataframe(df)
        
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()