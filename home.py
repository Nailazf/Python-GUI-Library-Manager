import time
import sys
import os
import datetime
import streamlit as st
from PIL import Image
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import uuid

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'perpustakaan'
}

# Initialize directories
IMAGES_DIR = "./assets/images"
INVOICES_DIR = "./assets/invoices"
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(INVOICES_DIR, exist_ok=True)

@st.cache_resource
def init_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# ==== FUNGSI BUKU ====
def get_buku():
    conn = init_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, 
                   jumlah_tersedia, jumlah_total
            FROM buku 
            WHERE status = 'active'
            ORDER BY judul
        """)
        daftar_buku = cursor.fetchall() 
        cursor.close()
        return daftar_buku
    except Error as e:
        st.error(f"Error fetching buku: {e}")
        return []

def get_available_buku():
    conn = init_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, jumlah_tersedia
            FROM buku 
            WHERE status = 'active' AND jumlah_tersedia > 0
            ORDER BY judul
        """)
        buku_tersedia = cursor.fetchall() 
        cursor.close()
        return buku_tersedia
    except Error as e:
        st.error(f"Error fetching available buku: {e}")
        return []

# ==== FUNGSI ANGGOTA ====
def get_anggota():
    conn = init_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nama, email, phone, alamat, tanggal_daftar
            FROM anggota 
            WHERE status = 'active'
            ORDER BY nama
        """)
        daftar_anggota = cursor.fetchall() 
        cursor.close()
        return daftar_anggota
    except Error as e:
        st.error(f"Error fetching anggota: {e}")
        return []

def add_anggota(nama, email, phone, alamat):
    conn = init_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO anggota (nama, email, phone, alamat)
            VALUES (%s, %s, %s, %s)
        """, (nama, email, phone, alamat))
        conn.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"Error adding anggota: {e}")
        return False

# ==== LOAN FUNCTIONS  ====
def create_loan(book_id, member_id, tanggal_pinjam, tanggal_kembali):
    conn = init_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Insert loan record
        cursor.execute("""
            INSERT INTO loans (book_id, member_id, tanggal_pinjam, tanggal_kembali, status)
            VALUES (%s, %s, %s, %s, 'dipinjam')
        """, (book_id, member_id, tanggal_pinjam, tanggal_kembali))
        
        # Update buku availability
        cursor.execute("""
            UPDATE buku 
            SET jumlah_tersedia = jumlah_tersedia - 1
            WHERE id = %s
        """, (book_id,))
        
        # Commit transaction
        cursor.execute("COMMIT")
        cursor.close()
        return True
    except Error as e:
        cursor.execute("ROLLBACK")
        st.error(f"Error creating loan: {e}")
        return False

def get_active_loans():
    conn = init_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.id, l.tanggal_pinjam, l.tanggal_kembali, l.status,
                   b.judul, b.pengarang,
                   m.nama as nama_peminjam, m.email
            FROM loans l
            JOIN buku b ON l.book_id = b.id 
            JOIN anggota m ON l.member_id = m.id 
            WHERE l.status = 'dipinjam'
            ORDER BY l.tanggal_kembali
        """)
        loans = cursor.fetchall()
        cursor.close()
        return loans
    except Error as e:
        st.error(f"Error fetching active loans: {e}")
        return []

def return_book(loan_id):
    conn = init_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("START TRANSACTION")
        
        # Get book_id from loan
        cursor.execute("SELECT book_id FROM loans WHERE id = %s", (loan_id,))
        book_id = cursor.fetchone()[0]
        
        # Update loan status
        cursor.execute("""
            UPDATE loans 
            SET status = 'dikembalikan'
            WHERE id = %s
        """, (loan_id,))
        
        # Update buku availability
        cursor.execute("""
            UPDATE buku 
            SET jumlah_tersedia = jumlah_tersedia + 1
            WHERE id = %s
        """, (book_id,))
        
        cursor.execute("COMMIT")
        cursor.close()
        return True
    except Error as e:
        cursor.execute("ROLLBACK")
        st.error(f"Error returning book: {e}")
        return False

def get_loan_history():
    conn = init_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.id, l.tanggal_pinjam, l.tanggal_kembali, l.status,
                   b.judul, b.pengarang,
                   m.nama as nama_peminjam, m.email
            FROM loans l
            JOIN buku b ON l.book_id = b.id 
            JOIN anggota m ON l.member_id = m.id 
            ORDER BY l.tanggal_pinjam DESC
            LIMIT 100
        """)
        loans = cursor.fetchall()
        cursor.close()
        return loans
    except Error as e:
        st.error(f"Error fetching loan history: {e}")
        return []

# ==== STREAMLIT APP ====
st.set_page_config(page_title="Perpustakaan Minimalism", page_icon="📚", layout="wide")

# Sidebar Navigation
st.sidebar.title("📚 Perpustakaan Minimalism")
pages = {
    "Home Page": "🏠",
    "Form Pinjam": "📝",
    "Form Pengembalian": "↩️",
    "Cetak Invoice": "🧾",
    "Manajemen Anggota": "👥",
    "Laporan": "📊",
    "Peraturan": "📋"
}

selected_page = st.sidebar.selectbox("Pilih Menu", list(pages.keys()), format_func=lambda x: f"{pages[x]} {x}")

# ==== HOME PAGE ====
if selected_page == "Home Page":
    st.title("📚Selamat Datang Di Perpustakaan")
    st.title("📚Minimalism")
    st.write("Berikut ini adalah daftar buku yang tersedia di perpustakaan kami")
    
    daftar_buku = get_buku() 
    
    if daftar_buku:
        # Display buku in columns (3 per row)
        for i in range(0, len(daftar_buku), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(daftar_buku):
                    buku = daftar_buku[i + j] 
                    
                    # Try to load image
                    try:
                        image_path = f"./assets/images/{buku['id']}.jpg"
                        if os.path.exists(image_path):
                            image = Image.open(image_path)
                        else:
                            image = Image.new('RGB', (200, 300), color='lightgray')
                    except:
                        image = Image.new('RGB', (200, 300), color='lightgray')
                    
                    with col:
                        st.image(image, width=200)
                        st.write(f"**{buku['judul']}**")
                        st.write(f"Pengarang: {buku['pengarang']}")
                        st.write(f"Kategori: {buku['kategori']}")
                        
                        if buku['jumlah_tersedia'] > 0:
                            st.success(f"Tersedia {buku['jumlah_tersedia']} dari {buku['jumlah_total']} buku")
                        else:
                            st.error("Tidak Tersedia")
                        
                        st.write("---")
    else:
        st.info("Tidak ada buku yang tersedia.")

# ==== FORM PINJAM ====
elif selected_page == "Form Pinjam":
    st.title("📝 Menu Peminjaman Buku")
    st.write("Silahkan Masukkan Data Diri Anda")
    
    # Get available buku and anggota
    available_buku = get_available_buku() 
    daftar_anggota = get_anggota() 
    
    if not available_buku:
        st.warning("Tidak ada buku yang tersedia untuk dipinjam.")
    elif not daftar_anggota:
        st.warning("Tidak ada anggota terdaftar. Silakan daftar di menu Manajemen Anggota.")
    else:
        with st.form("form_pinjam"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Anggota selection
                member_options = {f"{m['nama']} ({m['email']})": m['id'] for m in daftar_anggota} 
                selected_member = st.selectbox("Pilih Anggota", list(member_options.keys()))
                
                # Buku selection
                book_options = {f"{b['judul']} - {b['pengarang']} (Tersedia: {b['jumlah_tersedia']})": b['id'] for b in available_buku} 
                selected_book = st.selectbox("Pilih Judul Buku", list(book_options.keys()))
            
            with col2:
                tanggal_pinjam = st.date_input("Tanggal Peminjaman", value=datetime.now().date())
                tanggal_kembali = st.date_input("Tanggal Kembali", value=datetime.now().date() + timedelta(days=7))
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                member_id = member_options[selected_member]
                book_id = book_options[selected_book]
                
                if create_loan(book_id, member_id, tanggal_pinjam, tanggal_kembali):
                    st.success("✅ Peminjaman berhasil dicatat!")
                    st.balloons()
                else:
                    st.error("❌ Gagal mencatat peminjaman.")

# ==== FORM PENGEMBALIAN ====
elif selected_page == "Form Pengembalian":
    st.title("↩️ Menu Pengembalian Buku")
    st.write("Silahkan Pilih Buku yang Akan Dikembalikan")
    
    active_loans = get_active_loans()
    
    if not active_loans:
        st.info("Tidak ada buku yang sedang dipinjam.")
    else:
        st.write("**Daftar Buku yang Sedang Dipinjam:**")
        
        for loan in active_loans:
            with st.expander(f"📖 {loan['judul']} - {loan['nama_peminjam']}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Judul:** {loan['judul']}")
                    st.write(f"**Pengarang:** {loan['pengarang']}")
                    st.write(f"**Peminjam:** {loan['nama_peminjam']}")
                    st.write(f"**Email:** {loan['email']}")
                
                with col2:
                    st.write(f"**Tgl Pinjam:** {loan['tanggal_pinjam']}")
                    st.write(f"**Tgl Kembali:** {loan['tanggal_kembali']}")
                    
                    # Check if overdue
                    if loan['tanggal_kembali'] < datetime.now().date():
                        st.error("⚠️ TERLAMBAT")
                    else:
                        st.success("✅ Tepat Waktu")
                
                with col3:
                    if st.button("↩️ Kembalikan", key=f"return_{loan['id']}"):
                        if return_book(loan['id']):
                            st.success("Buku berhasil dikembalikan!")
                            st.rerun()
                        else:
                            st.error("Gagal mengembalikan buku.")

# ==== CETAK INVOICE ====
elif selected_page == "Cetak Invoice":
    st.title("🧾 Cetak Invoice")
    st.write("Laporan Peminjaman dan Pengembalian Buku")
    
    loan_history = get_loan_history()
    
    if loan_history:
        # Convert to DataFrame for easy display
        df = pd.DataFrame(loan_history)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter Status", ["Semua", "dipinjam", "dikembalikan"])
        with col2:
            # Added a simple month filter logic
            current_month_start = datetime.now().date().replace(day=1)
            last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
            
            month_options = {
                "Semua": "all",
                "Bulan ini": "current_month",
                "Bulan lalu": "last_month"
            }
            month_filter_selection = st.selectbox("Filter Bulan", list(month_options.keys()))
            
            filtered_df = df.copy()

            if status_filter != "Semua":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            if month_options[month_filter_selection] == "current_month":
                filtered_df = filtered_df[pd.to_datetime(filtered_df['tanggal_pinjam']).dt.to_period('M') == pd.Period(datetime.now().date(), 'M')]
            elif month_options[month_filter_selection] == "last_month":
                filtered_df = filtered_df[pd.to_datetime(filtered_df['tanggal_pinjam']).dt.to_period('M') == pd.Period(last_month_start, 'M')]
        
        st.write("**Riwayat Peminjaman:**")
        st.dataframe(filtered_df[['judul', 'pengarang', 'nama_peminjam', 'tanggal_pinjam', 'tanggal_kembali', 'status']])
        
        # Statistics
        st.write("**Statistik:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Peminjaman", len(filtered_df))
        with col2:
            st.metric("Sedang Dipinjam", len(filtered_df[filtered_df['status'] == 'dipinjam']))
        with col3:
            st.metric("Sudah Dikembalikan", len(filtered_df[filtered_df['status'] == 'dikembalikan']))
        
        # Export to CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"invoice_perpustakaan_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Belum ada riwayat peminjaman.")

# ==== MANAJEMEN ANGGOTA ====
elif selected_page == "Manajemen Anggota":
    st.title("👥 Manajemen Anggota")
    
    tab1, tab2 = st.tabs(["📋 Daftar Anggota", "➕ Tambah Anggota"])
    
    with tab1:
        st.write("**Daftar Anggota Perpustakaan:**")
        daftar_anggota = get_anggota() 
        
        if daftar_anggota:
            df_members = pd.DataFrame(daftar_anggota) 
            st.dataframe(df_members)
        else:
            st.info("Belum ada anggota terdaftar.")
    
    with tab2:
        st.write("**Daftarkan Anggota Baru:**")
        
        with st.form("add_member"):
            nama = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            phone = st.text_input("No. Telepon")
            alamat = st.text_area("Alamat")
            
            submitted = st.form_submit_button("➕ Daftarkan")
            
            if submitted:
                if nama and email:
                    if add_anggota(nama, email, phone, alamat): 
                        st.success("✅ Anggota berhasil didaftarkan!")
                        st.balloons()
                    else:
                        st.error("❌ Gagal mendaftarkan anggota.")
                else:
                    st.error("❌ Nama dan email wajib diisi.")

# ==== LAPORAN ====
elif selected_page == "Laporan":
    st.title("📊 Laporan Perpustakaan")
    
    # Get data for reports
    daftar_buku = get_buku() 
    daftar_anggota = get_anggota() 
    loans = get_loan_history()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Buku", len(daftar_buku)) 
    with col2:
        st.metric("Total Anggota", len(daftar_anggota)) 
    with col3:
        active_loans = [l for l in loans if l['status'] == 'dipinjam']
        st.metric("Buku Dipinjam", len(active_loans))
    with col4:
        available_buku_count = sum([b['jumlah_tersedia'] for b in daftar_buku]) 
        st.metric("Buku Tersedia", available_buku_count)
    
    # Charts
    if loans:
        st.subheader("📈 Grafik Peminjaman")
        
        # Monthly loan chart
        df_loans = pd.DataFrame(loans)
        df_loans['tanggal_pinjam'] = pd.to_datetime(df_loans['tanggal_pinjam'])
        df_loans['month'] = df_loans['tanggal_pinjam'].dt.to_period('M')
        
        monthly_loans = df_loans.groupby('month').size().reset_index(name='count')
        monthly_loans['month'] = monthly_loans['month'].astype(str)
        
        st.bar_chart(monthly_loans.set_index('month')['count'])
        
        # Popular buku
        st.subheader("📚 Buku Paling Populer")
        popular_buku = df_loans.groupby('judul').size().reset_index(name='count') 
        popular_buku = popular_buku.sort_values('count', ascending=False).head(10)
        st.dataframe(popular_buku)

# ==== PERATURAN ====
elif selected_page == "Peraturan":
    st.title("📋 Peraturan Perpustakaan")
    st.write("Berikut adalah peraturan yang berlaku di Perpustakaan Minimalism:")
    
    st.markdown("""
    ### 📖 Peraturan Umum
    1. **Registrasi Anggota**: Setiap peminjam harus terdaftar sebagai anggota perpustakaan
    2. **Kartu Anggota**: Wajib membawa kartu anggota atau ID yang valid
    3. **Jam Operasional**: Senin-Jumat 08:00-17:00, Sabtu 08:00-12:00
    
    ### 📚 Peraturan Peminjaman
    1. **Maksimal Peminjaman**: 3 buku per anggota
    2. **Masa Peminjaman**: 7 hari kerja
    3. **Perpanjangan**: Dapat diperpanjang 1x untuk 7 hari
    4. **Reservasi**: Buku yang sedang dipinjam dapat direservasi
    
    ### ⚠️ Sanksi dan Denda
    1. **Keterlambatan**: Rp 1,000 per hari per buku
    2. **Kehilangan**: Ganti buku yang sama atau senilai harga buku
    3. **Kerusakan**: Ganti biaya perbaikan atau penggantian
    4. **Suspesi**: Anggota dapat disuspend jika melanggar peraturan
    
    ### 🔒 Kebijakan Keamanan
    1. **Tas dan Jaket**: Dititipkan di loker atau penitipan
    2. **Makanan dan Minuman**: Tidak diperbolehkan di ruang baca
    3. **Kebisingan**: Jaga ketenangan dan tidak mengganggu
    4. **Telepon**: Mode silent atau gunakan di area yang disediakan
    """)

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()