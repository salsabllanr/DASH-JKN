# main.py
import streamlit as st
import pandas as pd

# Impor modul yang telah kita buat
from analysis import text
import config
from modules import information, graphics

# --- INISIALISASI ---
# 1. Atur konfigurasi halaman dan CSS
config.set_page_config()
config.load_custom_css() # Fungsi ini yang akan membaca style.css

# 2. Inisialisasi session state
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "information"
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
# 3. Siapkan data sampel
# sample_reviews = data.generate_sample_data()
data = pd.read_csv('dataset/datafix.csv')
# --- KOMPONEN UI UTAMA ---
# Header
st.markdown('<div class="header-title"><h1>📱 JKN Sentiment Analysis Dashboard</h1></div>', unsafe_allow_html=True)

# Sidebar untuk navigasi cepat
with st.sidebar:
    st.header("🚀 Quick Access")
    st.write(f"**Dataset Size**: {len(data):,} reviews")
    if st.button("📄 Information"):
        st.session_state.active_menu = "information"
    if st.button("📈 View Graphics"):
        st.session_state.active_menu = "graphics"
    if st.button("🔮 Run Analysis"):
        st.session_state.active_menu = "analysis"

# --- LOGIKA NAVIGASI HALAMAN ---
# Panggil fungsi `show()` dari halaman yang sesuai
if st.session_state.active_menu == "graphics":
    graphics.show(data)
elif st.session_state.active_menu == "analysis":
    text.show()
elif st.session_state.active_menu == "information":
    information.show(data)

# Footer
st.markdown("""
<div class="footer fade-in">
    <p><strong>JKN Sentiment Analysis Dashboard</strong></p>
    <p>Developed for academic and research purposes.</p>
</div>
""", unsafe_allow_html=True)