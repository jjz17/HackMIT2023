import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
from terra_utils import get_daily_data, extract_relevant_features
from bocd_utils import bocd_analysis
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def generate_date_range(start_date, end_date):
    # Generate a list of dates within the specified range
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    return date_range

def select_elements_by_indices(original_list, indices):
    selected_elements = [original_list[i] for i in indices]
    return selected_elements

# Create a Streamlit web app
st.title("AnomaLife :seedling:")
st.subheader("Your health tracker's careful companion")

st.divider()

st.set_option("deprecation.showPyplotGlobalUse", False)

# Input fields
user_id = st.text_input("User ID", "c62f231d-69cf-44f7-ba46-93c9e4de3ccd")
# User input: Start Date
start_date = st.date_input("Start Date", datetime.strptime("2023-08-01", "%Y-%m-%d"))
# User input: End Date
end_date = st.date_input("End Date", datetime.strptime("2023-09-10", "%Y-%m-%d"))

date_range = generate_date_range(start_date, end_date)


st.divider()

# Added a boolean flag to track if charts are displayed
charts_displayed = False

# Format dates as strings
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

fastapi_endpoint_url = "http://localhost:8000/get_anomaly_report"
response = requests.get(
    fastapi_endpoint_url,
    params={"user_id": user_id, "start_date": start_date_str, "end_date": end_date_str},
)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    st.subheader("Personal Data Snapshot")

    # st.write("Received JSON data:")
    # st.write(data)

    if data["need_to_process_json"]:
        # Extract relevant data from Terra API json response and save to csv
        extract_relevant_features()

    line_df = pd.read_csv(
        "/Users/jasonzhang/Documents/PersonalProjects/HackMIT2023/jason/tracker_data.csv"
    )

    # Create a date range
    # Truncate dataframe if necessary
    if len(line_df) > data["num_days"]:
        line_df = line_df.head(data["num_days"])


    pd_date_range = pd.date_range(start=start_date, end=end_date)
    dated_df = line_df.set_index(pd_date_range)

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Quick facts")
        st.markdown(':green[Days of data: ]')
        st.write(f"{data['num_days']}")
        st.markdown(':green[API response message: ]')
        st.write(f"{data['message']}")

    with col2:
        # st.header("A dog")
        # st.image("https://static.streamlit.io/examples/dog.jpg")
        st.caption("**Explore your personal data:**")
        st.write(dated_df)
        # Add a download button
        csv_data = dated_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name='downloaded_personal_data.csv',
            mime='text/csv'
)

    # Display charts if the data has been retrieved
    if charts_displayed:
        # Display charts until Exit button is clicked
        st.write("Charts displayed. Modify inputs and click Submit again to update.")
    else:

        def display_line_and_scatter_plot(line_df, selected_column, bocd_ch):
            if selected_column not in line_df.columns:
                st.error(f"Invalid column selected: {selected_column}. Choose a valid column.")
                return

            column_data = bocd_analysis(line_df[selected_column], constant_hazard=bocd_ch)

            # Create a Plotly figure with a line plot and a scatter plot
            fig = go.Figure()
            
            # Add the line plot
            fig.add_trace(go.Scatter(x=date_range, y=column_data["arr"].tolist(), mode='lines', name='Your Historical Trend'))
            
            anomaly_dates = select_elements_by_indices(date_range, column_data["index_changes"].tolist())

            # Add the scatter plot
            fig.add_trace(go.Scatter(
                x=anomaly_dates,
                y=column_data["arr"][column_data["index_changes"]].tolist(), mode='markers', name='Anomaly Change Points', 
                marker=dict(color="green", size=15)))

            fig.update_layout(title=f'Your change over time for {selected_column}',
                            # xaxis_title='X-axis',
                            # yaxis_title='Y-axis'
                            )
        

            st.plotly_chart(fig)

        st.divider()

        # Streamlit app
        st.title("Anomaly Detection Chart")

        # Select a column
        selected_column = st.selectbox('Select a metric of interest:', line_df.columns)

        detection_algorithm = st.selectbox("Choose an anomaly detection algorithm:", ["Z-Score", "BOCD", "Isolation Forest", "One-Class SVM", "Variational Autoencoder"], index=1)

        # Slider for the BOCD constant hazard hyperparameter
        bocd_constant_hazard_param = st.slider("BOCD Constant Hazard Hyperparameter (Expected likelihood of a change point event):", 0, 10, 100)

        display_line_and_scatter_plot(line_df, selected_column, bocd_constant_hazard_param)

        # Update the flag to indicate charts have been displayed
        charts_displayed = True

else:
    st.write(f"Failed to retrieve data. Status code: {response.status_code}")
