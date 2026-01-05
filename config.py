import streamlit as st

def set_page_config():
    """Menetapkan konfigurasi dasar halaman Streamlit."""
    st.set_page_config(
        page_title="JKN Sentiment Analysis Dashboard",
        page_icon="📱",
        layout="wide"
    )

def load_custom_css():
    """
    Membaca file style.css dan menyisipkannya ke dalam aplikasi Streamlit.
    Ini memisahkan logika styling dari logika aplikasi.
    """
    try:
        # Buka file style.css
        with open("style.css", "r") as f:
            # Baca seluruh konten file
            css_content = f.read()
        
        # Gunakan st.markdown untuk menyisipkan CSS ke dalam halaman
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error: style.css file not found. Please ensure it's in the same directory as main.py.")
