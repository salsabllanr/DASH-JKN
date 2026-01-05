import streamlit as st
import time

from api import predict_sentiment
from analysis.history import save_history, render_history
from analysis.upload import render_upload


def show():
    # =====================
    # LOAD CSS
    # =====================
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.header("🔍 Sentiment Analysis with SVM")

    # =====================
    # SESSION STATE
    # =====================
    if "user_text" not in st.session_state:
        st.session_state.user_text = ""

    # =====================
    # TABS
    # =====================
    tab1, tab2 = st.tabs(["Single Text Analysis", "Batch Upload (CSV)"])

    # ==============================================================
    # TAB 1: SINGLE TEXT ANALYSIS
    # ==============================================================
    with tab1:
        st.write("Enter a review to predict its sentiment using our SVM model.")

        with st.form("single_text_form", clear_on_submit=False):
            user_text = st.text_input(
                "Review Text",
                value=st.session_state.user_text,
                placeholder="e.g., The app is amazing and helpful!",
                key="review_text_input"
            )
            submit = st.form_submit_button("🚀 Predict Sentiment")

        if submit:
            st.session_state.user_text = user_text

            if not user_text.strip():
                st.warning("⚠️ Please enter a review.")
            else:
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.005)
                    progress.progress(i + 1)
                progress.empty()

                success, result = predict_sentiment(user_text)

                if success:
                    value = result.get("sentimen")
                    label = "Positive" if value == 1 else "Negative"
                    css_class = "result-positive" if value == 1 else "result-negative"
                    icon = "➕" if value == 1 else "➖"

                    st.markdown(
                        f"""
                        <div class="result-box {css_class}">
                            {icon} Predicted Sentiment: {label}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    save_history(user_text, label, value)

    # ==============================================================
    # TAB 2: BATCH CSV (MODULE)
    # ==============================================================
    with tab2:
        render_upload()

    # ==============================================================
    # HISTORY SECTION
    # ==============================================================
    render_history()
