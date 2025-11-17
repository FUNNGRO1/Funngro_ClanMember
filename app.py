import streamlit as st
import re
import pandas as pd
from io import StringIO

st.title("WhatsApp Group Join/Left Tracker (Date Filter)")

uploaded_file = st.file_uploader("Upload WhatsApp .txt chat file", type=["txt"])

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    # WhatsApp pattern
    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) - (.*)"

    rows = []

    for line in text.split("\n"):
        match = re.match(pattern, line)
        if match:
            date, time, message = match.groups()
            full_datetime = pd.to_datetime(date + " " + time)

            # Only detect join/left messages
            if "added" in message.lower() or "left" in message.lower() or "removed" in message.lower():
                rows.append([full_datetime, message])

    df = pd.DataFrame(rows, columns=["datetime", "message"])

    # Apply date filter
    mask = (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
    filtered_df = df[mask]

    st.write("Filtered Results", filtered_df)

    # Download
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download Filtered Data", csv, "filtered_data.csv")
