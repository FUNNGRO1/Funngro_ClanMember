import streamlit as st
import pandas as pd
from io import StringIO, BytesIO

# -------------------------------
# Title
# -------------------------------
st.title("📅 Date Range Data Extractor")
st.write("Upload your CSV → Select date range → Download filtered data")

# -------------------------------
# Upload Section
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Date Inputs
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

# -------------------------------
# Processing
# -------------------------------
if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Ensure date column exists
    if "date" not in df.columns:
        st.error("❌ No 'date' column found in the uploaded file.")
        st.stop()

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Filter by date range
    mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    # Display Results
    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)

    # -------------------------------
    # CSV Download
    # -------------------------------
    csv_data = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    # -------------------------------
    # XLSX Download
    # -------------------------------
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        filtered_df.to_excel(writer, index=False)

    st.download_button(
        label="⬇ Download Filtered Excel (XLSX)",
        data=output.getvalue(),
        file_name="filtered_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
