import streamlit as st
from database import init_db, get_user_from_db, add_user_to_db
from auth import hash_password_sha1, verify_password_sha1
from PIL import Image

st.set_page_config(page_title="Pusat Kriptografi", layout="wide")

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
    st.title("Tugas Akhir Kriptografi 🔐")
    st.subheader("Silakan Login atau Registrasi")

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
        st.header("Registrasi")
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
                    st.error(f"Username '{reg_username}' sudah terdaftar.")

# Tampilan Setelah Login
else:
    st.sidebar.success(f"Selamat datang, {st.session_state['username']}!")
    
    st.title(f"Selamat Datang di Dashboard Kriptografi, {st.session_state['username']}!")
    st.write("Ini adalah halaman utama untuk proyek Tugas Akhir Kriptografi.")
    st.divider() 

    # Informasi Kelompok
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
    st.header("Algoritma yang Digunakan")
    st.markdown("""
    Proyek ini mengimplementasikan beberapa algoritma kriptografi sesuai dengan spesifikasi tugas:
    * **Login (Hashing Password):** `SHA-1`
    * **Database History (Enkripsi Log):** `DES`
    * **Super Enkripsi (Teks):** `Vigenere Cipher + Blowfish`
    * **Enkripsi File (Dokumen/Gambar/dll):** `CAST-128`
    * **Steganografi (Pesan di Gambar):** `LSB (Least Significant Bit)`
    """)
    
    st.divider()

    # Panduan Penggunaan
    st.header("Panduan Penggunaan")
    with st.expander("Klik di sini untuk melihat panduan"):
        st.markdown("""
        Anda dapat menggunakan menu di sidebar kiri untuk menavigasi fitur-fitur berikut:
        
        1.  **Home:** Halaman ini yang sedang Anda lihat.
        2.  **Enkripsi File:** Menu untuk mengamankan file (PDF, DOCX, JPG, dll) menggunakan algoritma **CAST-128**. Masukkan file dan kunci (tepat 16 byte) untuk mengenkripsi atau mendekripsi.
        3.  **Steganografi LSB:** Menu untuk menyembunyikan pesan teks rahasia ke dalam gambar `.png`. Anda juga bisa mengungkap pesan dari gambar stego.
        4.  **History:** Melihat catatan/riwayat semua aktivitas enkripsi dan dekripsi yang telah Anda lakukan. Log ini dienkripsi di database menggunakan **DES**.
        5.  **Super Enkripsi:** Menu untuk enkripsi teks *multi-lapis*. Pesan Anda akan dienkripsi dulu dengan **Vigenere Cipher**, lalu hasilnya dienkripsi lagi dengan **Blowfish**.
        6.  **Logout:** Tombol di sidebar untuk keluar dari sesi Anda.
        """)
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = 0
        st.rerun()