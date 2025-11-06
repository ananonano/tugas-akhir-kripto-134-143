# Nama file: Home.py
import streamlit as st
from database import init_db, get_user_from_db, add_user_to_db
from auth import hash_password_sha1, verify_password_sha1
from PIL import Image

st.set_page_config(page_title="AmanKripto", layout="wide")

# Inisialisasi database saat aplikasi pertama kali jalan
try:
    init_db()
except Exception as e:
    st.error(f"Gagal terhubung ke database MySQL. Pastikan database server (XAMPP/MAMP) Anda berjalan. Error: {e}")
    st.stop()

# Manajemen Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = 0

# Tampilan Sebelum Login
if not st.session_state['logged_in']:
    st.title("AmanKripto 🔐: Solusi Keamanan Data Keuangan")
    st.subheader("Silakan Login atau Registrasi Akun Anda")

    tab1, tab2 = st.tabs(["Login", "Registrasi"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            user = get_user_from_db(login_username)
            if user and verify_password_sha1(login_password, user[2]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = user[1]
                st.session_state['user_id'] = user[0]
                st.rerun() # Memuat ulang halaman ke state "logged in"
            else:
                st.error("Username atau password salah.")

    with tab2:
        st.header("Registrasi Akun Baru")
        reg_username = st.text_input("Username Baru", key="reg_user")
        reg_password = st.text_input("Password Baru", type="password", key="reg_pass")
        reg_password_confirm = st.text_input("Konfirmasi Password", type="password", key="reg_pass_confirm")
        
        if st.button("Daftar"):
            if not reg_username or not reg_password:
                st.error("Username dan password tidak boleh kosong.")
            elif reg_password != reg_password_confirm:
                st.error("Password tidak cocok.")
            else:
                hashed_pass = hash_password_sha1(reg_password)
                if add_user_to_db(reg_username, hashed_pass):
                    st.success(f"Akun '{reg_username}' berhasil dibuat! Silakan login.")
                else:
                    # Error ditangani oleh add_user_to_db
                    pass

# Tampilan Setelah Login
else:
    st.sidebar.success(f"Selamat datang, {st.session_state['username']}!")
    
    st.title(f"Selamat Datang di Dashboard Keamanan Finansial, {st.session_state['username']}!")
    st.write("Gunakan menu di sidebar untuk mengamankan data keuangan Anda.")
    st.divider() 

    # Informasi Kelompok (Biarkan, ini info Anda)
    st.markdown("<h2 style='text-align: center;'>Kelompok 8</h2>", unsafe_allow_html=True)
    st.write("")
    margin_kiri, col1, col2, margin_kanan = st.columns([2, 2, 2, 2]) 
    TARGET_WIDTH = 250
    with col1:
        try:
            img_danang = Image.open("danang.png") 
            w_percent = (TARGET_WIDTH / float(img_danang.size[0]))
            h_size = int((float(img_danang.size[1]) * float(w_percent)))
            img_danang_resized = img_danang.resize((TARGET_WIDTH, h_size), Image.LANCZOS)
            st.image(img_danang_resized)
        except Exception as e:
            st.warning(f"Gagal memuat foto Danang: {e}. Pastikan file 'danang.jpg' ada.")
        st.info("**Danang Adiwibowo**\n\nNIM: 123230143")
    with col2: 
        try:
            img_aksa = Image.open("aksa.png")
            w_percent = (TARGET_WIDTH / float(img_aksa.size[0]))
            h_size = int((float(img_aksa.size[1]) * float(w_percent)))
            img_aksa_resized = img_aksa.resize((TARGET_WIDTH, h_size), Image.LANCZOS)
            st.image(img_aksa_resized)
        except Exception as e:
            st.warning(f"Gagal memuat foto Aksa: {e}")
        st.info("**Mohammad Atilla Danadyaksa**\n\nNIM: 12320134")
    
    st.divider()

    # Informasi Algoritma yang Digunakan
    st.header("Metode Keamanan yang Digunakan")
    st.markdown("""
    Aplikasi ini mengamankan data Anda menggunakan beberapa metode kriptografi standar industri:
    * **Otentikasi Akun (Hashing):** `SHA-1` (Mengamankan kredensial login Anda).
    * **Log Audit (Enkripsi Log):** `DES` (Setiap aktivitas Anda dicatat dan dienkripsi untuk audit).
    * **Enkripsi Transaksi:** `Vigenere Cipher + Blowfish` (Metode 'Super Enkripsi' untuk data Pemasukan/Pengeluaran).
    * **Enkripsi Struk/Bukti:** `CAST-128` (Mengamankan file laporan, invoice, atau struk PDF/JPG).
    * **Sisip Data / Watermark:** `PVD` (Menyisipkan data audit atau watermark tak terlihat pada file gambar).
    """)
    
    st.divider()

    # Panduan Penggunaan
    st.header("Panduan Penggunaan")
    with st.expander("Klik di sini untuk melihat panduan"):
        st.markdown("""
        Anda dapat menggunakan menu di sidebar kiri untuk menavigasi fitur-fitur berikut:
        
        1.  **Home:** Halaman ini yang sedang Anda lihat.
        2.  **Catat Transaksi:** Menu untuk mencatat Pemasukan/Pengeluaran. Data (Tipe, Nominal, Keterangan) akan dienkripsi berlapis menggunakan **Vigenere + Blowfish**.
        3.  **Enkripsi Struk:** Menu untuk mengamankan file (PDF, JPG, dll) seperti bukti transfer atau invoice menggunakan **CAST-128**.
        4.  **Sisipkan Data (PVD):** Menu untuk menyembunyikan catatan rahasia (misal: ID transaksi) ke dalam gambar `.png` menggunakan **PVD**.
        5.  **Laporan Audit:** Melihat ringkasan total Pemasukan/Pengeluaran Anda, beserta riwayat lengkap semua aktivitas keamanan. Log ini dienkripsi di database menggunakan **DES**.
        6.  **Logout:** Tombol di sidebar untuk keluar dari sesi Anda.
        """)
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()