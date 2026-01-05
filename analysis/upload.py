import streamlit as st
import pandas as pd
from io import BytesIO

from api import predict_sentiment
from analysis.history import save_history


def render_upload():
    st.write("Upload a CSV file to classify the text in a specific column.")

    # =====================
    # SESSION STATE INIT
    # =====================
    if "uploaded_df" not in st.session_state:
        st.session_state.uploaded_df = None

    if "predicted_df" not in st.session_state:
        st.session_state.predicted_df = None

    # =====================
    # FILE UPLOADER
    # =====================
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        key="csv_uploader"
    )

    # =====================
    # LOAD FILE
    # =====================
    if uploaded_file is not None:
        st.session_state.uploaded_df = pd.read_csv(uploaded_file)
        st.session_state.predicted_df = None  # reset hasil lama

    # =====================
    # PREVIEW DATA
    # =====================
    if st.session_state.uploaded_df is not None:
        df = st.session_state.uploaded_df

        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)

        text_column = st.selectbox(
            "Select the column containing the text/reviews:",
            df.columns,
            key="csv_text_column"
        )

        col_process, col_cancel = st.columns([2, 1])

        # ---------- PROCESS ----------
        with col_process:
            if st.button("🚀 Process File and Predict", key="process_csv"):
                with st.spinner("Processing..."):
                    progress = st.progress(0)
                    predictions = []

                    for i, text in enumerate(df[text_column]):
                        success, result = predict_sentiment(text)

                        if success:
                            value = result.get("sentimen")
                            label = "Positive" if value == 1 else "Negative"
                            predictions.append(label)
                            save_history(text, label, value)
                        else:
                            predictions.append("Error")

                        progress.progress((i + 1) / len(df))

                    progress.empty()

                df_result = df.copy()
                df_result["predicted_sentiment"] = predictions
                st.session_state.predicted_df = df_result

                st.markdown(
                    "<div class='success-box'>✅ Processing complete.</div>",
                    unsafe_allow_html=True
                )

        # ---------- CANCEL ----------
        with col_cancel:
            if st.button("❌ Cancel Upload", key="cancel_csv", use_container_width=True):
                st.session_state.uploaded_df = None
                st.session_state.predicted_df = None
                st.rerun()

    # =====================
    # SHOW RESULT & DOWNLOAD (PERSISTENT)
    # =====================
    if st.session_state.predicted_df is not None:
        st.subheader("Processed Data with Predictions")
        st.dataframe(st.session_state.predicted_df, use_container_width=True)

        col_csv, col_excel = st.columns(2)

        with col_csv:
            st.download_button(
                "📄 Download CSV",
                st.session_state.predicted_df.to_csv(index=False).encode("utf-8"),
                "predicted_results.csv",
                "text/csv",
                use_container_width=True
            )

        with col_excel:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                st.session_state.predicted_df.to_excel(writer, index=False)

            st.download_button(
                "📊 Download Excel",
                excel_buffer.getvalue(),
                "predicted_results.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )