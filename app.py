import streamlit as st
import re
import pandas as pd

st.title("WhatsApp Group Join/Left Tracker (Advanced Parser + Date Filter)")

uploaded_file = st.file_uploader("Upload WhatsApp exported .txt chat", type=["txt"])

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) - (.*)"
    rows = []

    for line in text.split("\n"):
        match = re.match(pattern, line)
        if not match:
            continue

        date, time, message = match.groups()
        full_datetime = pd.to_datetime(date + " " + time)

        msg_lower = message.lower()

        # Detect join/left events
        if ("added" in msg_lower or 
            "removed" in msg_lower or 
            "left" in msg_lower or 
            "joined using" in msg_lower):

            # Extract number OR name
            number_match = re.search(r"\+?\d[\d\s\-]{7,}", message)
            if number_match:
                user = number_match.group().replace(" ", "")
            else:
                # Extract text before keywords
                user = re.split("added|removed|left|joined", message, flags=re.IGNORECASE)[0].strip()

            action = ""
            if "added" in msg_lower:
                action = "Joined"
            elif "joined using" in msg_lower:
                action = "Joined"
            elif "removed" in msg_lower:
                action = "Removed"
            elif "left" in msg_lower:
                action = "Left"

            rows.append([full_datetime, user, action, message])

    df = pd.DataFrame(rows, columns=["datetime", "user", "action", "raw_message"])

    # Date filter
    mask = (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
    filtered = df[mask]

    st.subheader("Filtered Results")
    st.write(filtered)

    csv_data = filtered.to_csv(index=False)
    st.download_button("Download Filtered CSV", csv_data, "filtered_data.csv")
