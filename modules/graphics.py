import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import date

def show(data):
    """Menampilkan halaman Grafik dengan visualisasi data."""
    st.header("📈 View Graphics")
    
    # --- PERBAIKAN FILTER: Menggunakan st.date_input untuk UX yang lebih baik ---
    st.markdown("---") # Garis pemisah
    st.subheader("🔎 Filter Data")
    
    # Pastikan kolom 'at' bertipe datetime
    if 'at' not in data.columns:
        st.error("Kolom 'at' (tanggal) tidak ditemukan di data.")
        st.stop()
        
    data['at'] = pd.to_datetime(data['at'])

    # Tentukan tanggal minimum dan maksimum dari data
    min_date = data['at'].min().date()
    max_date = data['at'].max().date()

    col1, col2 = st.columns(2) # Membagi filter menjadi 2 kolom
    with col1:
        sentiment_filter = st.radio(
            "Filter by Sentiment", 
            ["All", "POSITIVE", "NEGATIVE"], 
            horizontal=True,
            key="sentiment_radio"
        )
    try:
        with col2:
            # Widget input rentang tanggal
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            start_date, end_date = date_range
        
        # Validasi rentang tanggal
        if end_date < start_date:
            st.error("End date cannot be earlier than start date.")
            st.stop()


        # Konversi date kembali ke datetime untuk filtering
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)

        # Filter data berdasarkan tanggal dan sentimen
        filtered_data = data[
            (data['at'] >= start_datetime) &
            (data['at'] <= end_datetime)
        ]

        if sentiment_filter != "All":
            filtered_data = filtered_data[filtered_data['LABELING'] == sentiment_filter]

        st.markdown("---") # Garis pemisah
        
        # --- LOGIKA VISUALISASI ---
        if filtered_data.empty:
            st.warning("⚠️ No data matches your filters. Try adjusting the range.")
        else:
            # PIE CHART
            st.markdown('<div class="card fade-in"><h2>Sentiment Distribution</h2>', unsafe_allow_html=True)
            fig1 = px.pie(
                filtered_data,
                names="LABELING",
                color="LABELING",
                color_discrete_map={"POSITIVE": "#1a73e8", "NEGATIVE": "#d9534f"}
            )
            fig1.update_traces(textinfo='percent+label', textposition='inside')
            fig1.update_layout(showlegend=True, legend_title="Sentiment Category", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- PERBAIKAN: LINE CHART PER TANGGAL ---
            st.markdown('<div class="card fade-in"><h2>📈 Review Volume per Date</h2>', unsafe_allow_html=True)

            # 1. Buat DataFrame 'counts' dengan mengelompokkan data PER TANGGAL
            counts = filtered_data.groupby(filtered_data["at"].dt.date).size().reset_index(name="count")

            # 2. Periksa apakah DataFrame 'counts' kosong sebelum membuat grafik
            if counts.empty:
                st.write("Tidak ada data untuk ditampilkan pada periode yang dipilih.")
            else:
                # 3. Buat grafik GARIS (line chart) menggunakan Plotly
                fig_line = px.line(
                    counts,
                    x="at",
                    y="count",
                    markers=True,               # Tambahkan titik pada setiap data
                    line_shape="spline",        # Buat garis lebih halus
                    labels={"at": "Date", "count": "Number of Reviews"} # Label yang jelas
                )
                
                # 4. Sesuaikan tampilan grafik
                fig_line.update_traces(line=dict(color="#1a73e8", width=3)) # Warna dan ketebalan garis
                fig_line.update_layout(
                    title="Review Volume per Date", # Judul grafik
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Date",
                    yaxis_title="Number of Reviews"
                )
                
                st.plotly_chart(fig_line, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # WORD CLOUDS
            st.markdown('<div class="card fade-in"><h2>☁️ Word Clouds by Sentiment</h2>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="wordcloud-box"><h3>😊 Positive Reviews</h3>', unsafe_allow_html=True)
                pos_text = " ".join(review for review in filtered_data[filtered_data['LABELING'] == 'POSITIVE']['CONTENT'])
                if pos_text.strip():
                    wc = WordCloud(width=400, height=250, background_color="white", colormap="Blues").generate(pos_text)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No positive reviews in selection.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="wordcloud-box"><h3>😞 Negative Reviews</h3>', unsafe_allow_html=True)
                neg_text = " ".join(review for review in filtered_data[filtered_data['LABELING'] == 'NEGATIVE']['CONTENT'])
                if neg_text.strip():
                    wc = WordCloud(width=400, height=250, background_color="white", colormap="Reds").generate(neg_text)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No negative reviews in selection.")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="wordcloud-box"><h3>📄 All Reviews</h3>', unsafe_allow_html=True)
                all_text = " ".join(review for review in filtered_data['CONTENT'])
                if all_text.strip():
                    wc = WordCloud(width=400, height=250, background_color="white", colormap="viridis").generate(all_text)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No reviews in selection.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error('Data tanggal harus lengkap')