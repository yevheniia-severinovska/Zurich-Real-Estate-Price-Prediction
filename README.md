Zurich Real Estate Price Trends

An interactive data app that shows average condo prices per square meter in Zurich by district and predicts prices for 2025–2026 using simple linear regression.

Overview

This project uses Python and Streamlit to explore real estate price trends across Zurich. The user can select a district and view a clean, readable chart with predictions for the next two years.

Tech Stack

Python
pandas
NumPy
matplotlib
Streamlit

Files

app.py
Interactive Streamlit app. Loads cleaned data, filters by district, groups by year, applies linear regression, and plots the result.

data_cleaning.py
Script that prepares the dataset: renames columns, handles number formatting, removes invalid rows, and outputs clean_zurich_data.csv.

How It Works

User selects a district from the sidebar
The app filters and processes the data
A simple linear model predicts prices for 2025 and 2026
Results are shown in a line chart and summary messages

How to Run

pip install pandas numpy matplotlib streamlit
streamlit run app.py

Future Work

Evaluate predictions
Add a chatbot-helper
Analyze competitors


Author

Built as a first data science project by Yevheniia Severinovska learning Python and AI tools.

