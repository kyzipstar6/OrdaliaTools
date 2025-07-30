# streamlit_plot_app/plot_app.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io

st.set_page_config(page_title="Plot Uploader", layout="wide")

st.title("📈 Plot Uploader")
st.write("Upload your `.txt` or `.csv` simulation file and plot a selected column.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])

if uploaded_file:
    try:
        lines = uploaded_file.read().decode("utf-8").splitlines()
        column_index = st.number_input("Column index to plot (0-based)", min_value=0, value=6)
        data = []

        for line in lines[1:-1]:  # skip header and last line
            parts = line.strip().split()
            if len(parts) > column_index:
                try:
                    data.append(float(parts[column_index]))
                except ValueError:
                    pass

        fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
        ax.plot(range(len(data)), data)
        ax.set_title(f"Column {column_index} Plot")
        ax.set_ylim(0, 10)
        ax.grid(True)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Download Plot", buf.getvalue(), file_name="plot.png", mime="image/png")
    except Exception as e:
        st.error(f"Failed to process file: {e}")
