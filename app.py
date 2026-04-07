import streamlit as st
import requests
from datetime import datetime, date

st.title("MLB Daily Tracking Metrics Dashboard")

# Date selector: defaults to today
selected_date = st.date_input("Select a date", value=date.today())

# Format date for the API
date_str = selected_date.strftime("%Y-%m-%d")
api_url = f"https://statsapi.mlb.com/tools/status-page?date={date_str}"

# Add a common User-Agent header to mimic a standard browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fetch data when the date is selected
try:
    response = requests.get(api_url, headers=headers)
    # Print the status code to the dashboard for debugging
    st.write(f"API Response Status Code: {response.status_code}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
    else:
        st.error(f"API request failed with status code: {response.status_code}")
        st.error("This usually means the server is blocking the request. This is common when deploying on cloud platforms.")
        data = None

except requests.exceptions.RequestException as e:
    st.error(f"A network/connection error occurred: {e}")
    data = None

if data:
    st.subheader(f"Data for {date_str}")
    st.json(data)  # This will display the FULL API response for inspection
    
    # Display the metrics in a clean layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Pitches Tracked", data.get('pitchesTracked', 'N/A'))
        st.metric("Pitches with Spin Rate", data.get('pitchesWithSpinRate', 'N/A'))
        st.metric("BIP Tracked", data.get('bipTracked', 'N/A'))
        st.metric("Swings Tracked", data.get('swingsTracked', 'N/A'))
        
    with col2:
        st.metric("Batter Biomech", data.get('batterBiomech', 'N/A'))
        st.metric("Player Tracking", data.get('playerTracking', 'N/A'))
        st.metric("Pose Tracking", data.get('poseTracking', 'N/A'))
        
else:
    st.info("No data available to display. Check the error messages above.")
