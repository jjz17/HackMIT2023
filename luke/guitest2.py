import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Create a Streamlit web app
st.title("Anomaly Detector")

st.set_option('deprecation.showPyplotGlobalUse', False)

# Input fields
user_id = st.text_input("User ID")
start_time = st.text_input("Start Time")
end_time = st.text_input("End Time")

# Submit button
if st.button("Submit"):
    # Input validation
    if not user_id.isdigit():
        st.error("User ID must be a number")
    else:
        # Generate example data for the histogram
        data = np.random.normal(0, 1, 1000)

        # Display user inputs
        st.write(f"User ID: {user_id}")
        st.write(f"Start Time: {start_time}")
        st.write(f"End Time: {end_time}")

        # Plot and display the histogram
        st.write("Example Histogram")
        plt.hist(data, bins=30, edgecolor='black')
        plt.xlabel("Values")
        plt.ylabel("Frequency")
        st.pyplot()

# Exit button
if st.button("Exit"):
    st.stop()



