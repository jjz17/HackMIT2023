# AnomaLife

AnomaLife is a community health improvement project developed during
HackMIT 2023. Our team's goal is to create a suite of integrated systems to
improve community health and reduce the load on existing healthcare
infrastructure. This project is a collaboration between CJ, Luke, Jason, and
Vikrash.

Slides Link: https://docs.google.com/presentation/d/1riZoUY-gvzTnAkq94Iee_P480jm60Q6byfHW-VymHDY/edit#slide=id.g1e7bb606b76_3_174

## Table of Contents

- [AnomaLife](#anomalife)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Future Work](#future-work)
  - [Technologies Used](#technologies-used)
  - [Contributors](#contributors)

## Overview

AnomaLife aims to enhance community health by providing a comprehensive suite of
integrated systems. Our project interfaces with a wearable health tracking
device through the Terra API, processes the data, and provides insights through
an intuitive web interface. Additionally, we are exploring various future
enhancements, such as alternative choices for anomaly detection, integration
with healthcare provider tools, autonomous reporting during emergencies, and
automatic triaging support in emergency room settings.

## Features

- Seamless integration with wearable health tracking devices through the Terra
  API.
- Efficient data processing pipeline, converting JSON data to CSV for analysis.
- Anomaly detection using the BOCD algorithm for real-time health data
  monitoring.
- Interactive web interface powered by Streamlit for data exploration.
- Time series visualization with the Plotly library.
- Ongoing development of advanced features to enhance community health.

## Installation

To set up AnomaLife locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jjz17/HackMIT2023
   cd HackMIT2023
   ```

2. Install the required dependencies:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run services
   ```bash
   ngrok http 8000
   uvicorn jason.main:app --reload
   streamlit run jason/frontend.py
   ```

## Usage

- Use the user-friendly interface to connect to your Terra API account and
  retrieve health data from your wearable device.

- Explore time series data visualizations and anomaly detection results.

- Customize and fine-tune anomaly detection settings as needed.

## Future Work

Our vision for the future of AnomaLife includes the following exciting
enhancements:

- Implement alternative choices for anomaly detection to provide users with more
  options.
- Integrate our suite of systems with tools used by healthcare providers for
  seamless collaboration.
- Develop a feature for autonomously sending health reports to emergency service
  providers during emergencies.
- Utilize our analysis and tracking capabilities to help perform automatic
  triaging tasks in emergency room settings.

## Technologies Used

- python-terra - Python library for interfacing with the Terra API.
- Plotly - Python graphing library for creating interactive, publication-quality
  graphs.
- Streamlit - Python web app framework for creating custom web applications for
  data science and machine learning.
- Pandas - Python library for data science workflows

## Contributors

- CJ (GitHub: github.com/cjhi)
- Luke (GitHub: github.com/lhwitten)
- Jason (GitHub: github.com/jjz17)
- Vikrash (GitHub: github.com/rivcode)
