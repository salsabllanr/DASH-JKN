import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================
# KONFIGURASI
# =====================
HISTORY_FILE = "dataset/history.csv"
HISTORY_COLUMNS = ["timestamp", "review", "sentiment", "value"]

os.makedirs("dataset", exist_ok=True)


# =====================
# LOAD HISTORY (AMAN)
# =====================
def load_history():
    try:
        if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
            return pd.read_csv(HISTORY_FILE)
        return pd.DataFrame(columns=HISTORY_COLUMNS)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=HISTORY_COLUMNS)


# =====================
# SAVE HISTORY
# =====================
def save_history(text, sentiment, value=None):
    df = load_history()

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "review": text,
        "sentiment": sentiment,
        "value": value
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)


# =====================
# RENDER HISTORY UI
# =====================
def render_history():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📜 Analysis History")

    # ---------- INIT NOTIFICATION STATE ----------
    if "history_notice" not in st.session_state:
        st.session_state.history_notice = None

    # ---------- SHOW NOTIFICATION ----------
    if st.session_state.history_notice:
        st.markdown(
            f"<div class='success-box'>ℹ️ {st.session_state.history_notice}</div>",
            unsafe_allow_html=True
        )
        st.session_state.history_notice = None  # tampil sekali saja

    with st.expander("View Analysis History", expanded=True):

        col_refresh, spacer, col_clear = st.columns([2, 0.5, 2])

        # ---------- REFRESH ----------
        with col_refresh:
            if st.button("🔄 Refresh History", use_container_width=True):
                st.session_state.history_notice = "History refreshed successfully."
                st.rerun()

        # ---------- CLEAR ----------
        with col_clear:
            if st.button("🗑️ Clear History", use_container_width=True):
                pd.DataFrame(columns=HISTORY_COLUMNS).to_csv(
                    HISTORY_FILE, index=False
                )
                st.session_state.history_notice = "History has been cleared."
                st.rerun()

        # ---------- LOAD DATA ----------
        df_history = load_history()

        if df_history.empty:
            st.info("No analysis history yet.")
            return

        # ---------- SEARCH ----------
        search = st.text_input("Search History")

        if search.strip():
            df_history = df_history[
                df_history.apply(
                    lambda row: row.astype(str)
                    .str.contains(search, case=False)
                    .any(),
                    axis=1
                )
            ]

        st.dataframe(df_history, use_container_width=True)