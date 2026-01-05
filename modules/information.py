import streamlit as st
import pandas as pd

def show(data):
    """Menampilkan halaman Informasi."""
    st.header("ℹ️ Information")

    st.write("""
        This dashboard is designed to analyze public sentiment regarding the Mobile JKN app 
        using a Support Vector Machine (SVM) model.
        Below is an overview of the model and dataset used.
    """)

    # =====================
    # STATISTIK DATASET
    # =====================
    positive = data[data['LABELING'] == 'POSITIVE']
    negative = data[data['LABELING'] == 'NEGATIVE']

    total_positive = len(positive)
    total_negative = len(negative)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'''
            <div class="wordcloud-box">
                <h3>Total Review Positive</h3>
                <h1 style="color:#1a73e8; margin-top: -30px;">{total_positive}</h1>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'''
            <div class="wordcloud-box">
                <h3>Total Review Negative</h3>
                <h1 style="color:#d9534f; margin-top: -30px;">{total_negative}</h1>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # =====================
    # MODEL OVERVIEW
    # =====================
    st.subheader("📌 Model Overview")

    st.write("""
        - **Model Type:** Support Vector Machine (SVM)  
        - **Vectorizer:** TF-IDF  
        - **Dataset:** User reviews extracted from Google Play Store  
        - **Timeline:** 02 Desember 2025 – 14 Desember 2025  
    """)

    # =====================
    # MODEL PERFORMANCE (DARI HASIL EVALUASI)
    # =====================
    st.subheader("📊 Model Performance (SVM – Best Model)")

    accuracy = 0.9367
    precision = 0.9695
    recall = 0.9191
    f1_score = 0.9436

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", f"{accuracy:.2%}")
    col2.metric("Precision", f"{precision:.2%}")
    col3.metric("Recall", f"{recall:.2%}")
    col4.metric("F1-Score", f"{f1_score:.2%}")

    # =====================
    # DATASET SUMMARY
    # =====================
    st.subheader("📂 Dataset Summary")
    st.write(f"""
        The dataset consists of **{len(data):,} user reviews** collected using a scraping mechanism.
        Reviews are classified into:
        - **Positive sentiment**
        - **Negative sentiment**
    """)

    # =====================
    # SYSTEM CAPABILITIES
    # =====================
    st.subheader("⚙️ System Capabilities")
    st.write("""
        - Sentiment prediction for individual text inputs  
        - Visualization of sentiment trends  
        - Interactive dashboard filtering  
        - Word cloud representation  
    """)

    # =====================
    # DEVELOPER INFO
    # =====================
    st.subheader("📞 Developer Contact")
    st.write("""
        - **Name:** Adinda Salsabilla Naura  
        - **Email:** sblnr216@mail.com  
        - **Institution:** Universitas Mulawarman  
    """)
