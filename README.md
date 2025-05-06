
# 🏙️ Zurich Condo Price Trends

An interactive data app that shows average condo prices per square meter in Zurich by district and predicts prices for 2025–2026 using simple linear regression.

## 📈 Idea

One of the project’s goals was to explore how pricing trends could inform revenue potential — helping identify which timeframes or districts might offer the best return if a property were sold.

### ☁️ Overview

This project uses Python and Streamlit to explore real estate price trends across Zurich. The user can select a district and view a clean, readable chart with predictions for the next two years.

### ☁️ Tech Stack

- Python
- pandas
- NumPy
- matplotlib
- Streamlit

### ☁️ Files

- app.py
	Interactive Streamlit app. Loads cleaned data, filters by district, groups by year, applies linear regression, and plots the result.

 - data_cleaning.py 
	Script that prepares the dataset: renames columns, handles number formatting, removes invalid rows, and outputs clean_zurich_data.csv.

### ☁️ How It Works

User selects a district from the sidebar.
The app filters and processes the data.
A simple linear model predicts prices for 2025 and 2026.
Results are shown in a line chart and summary messages.
  
### ☁️ How to Run
  
    pip install pandas numpy matplotlib streamlit
    streamlit run app.py

### ☁️ Future Work

 1.  Evaluate the model
 2. Add a chatbot-helper
 3. Analyze competitors
  
### ☁️ Author

Built as a first data science project by Yevheniia Severinovska, a product designer learning Python and AI tools.