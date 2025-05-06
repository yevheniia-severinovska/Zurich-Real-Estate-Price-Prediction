import pandas as pd             # data handling
import streamlit as st          # web app UI
import matplotlib.pyplot as plt # plotting charts
import numpy as np              # math and modeling

# Load data into a DataFrame for easy filtering and analysis
df = pd.read_csv("clean_zurich_data.csv")

st.header("🏙️ Zurich Condo Price Trends (2009–2026)")

# --- Step 1: Prepare district list for sidebar selection ---

district_display = [
    "Zurich (Total)",
    "Kreis 1", " • Rathaus", " • Lindenhof",
    "Kreis 2", " • Wollishofen", " • Enge",
    "Kreis 3", " • Alt-Wiedikon", " • Friesenberg", " • Sihlfeld",
    "Kreis 4", " • Langstrasse", " • Hard",
    "Kreis 5", " • Gewerbeschule", " • Escher Wyss",
    "Kreis 6", " • Unterstrass", " • Oberstrass",
    "Kreis 7", " • Fluntern", " • Hottingen", " • Hirslanden", " • Witikon",
    "Kreis 8", " • Seefeld", " • Mühlebach", " • Weinegg",
    "Kreis 9", " • Albisrieden", " • Altstetten",
    "Kreis 10", " • Höngg", " • Wipkingen",
    "Kreis 11", " • Affoltern", " • Oerlikon", " • Seebach",
    "Kreis 12", " • Hirzenbach"
]

# Get a list of districts from the dataset to validate which ones are available
available_districts = df['district'].unique().tolist()

display_to_actual = {d: d for d in available_districts} # Dictionary(hash-map) with csv&displayed names

# Keeping only districts from the display list that exist in the dataset to avoid invalid sidebar options
full_display = []
for d in district_display:
    name = d.strip(" • ")                 
    if name in available_districts:
        full_display.append(d)
        display_to_actual[d] = name

# Adding sidebar radio buttons to select a district from the filtered and formatted list
selected_display = st.sidebar.radio("Select District", full_display, index=0)

# Get the real district name for filtering
selected_district = display_to_actual[selected_display]

# --- Step 2: Filter data for selected district ---

if selected_district == 'Zurich (Total)':
    df_selected = df.copy()
else:
    df_selected = df[df['district'] == selected_district]

# --- Step 3: Group data by year and calculate average price per m² ---

price_trend = df_selected.groupby("year")["price_per_m2"].mean().reset_index()

# --- Step 4: Predict price for 2025–2026 using simple linear regression ---

years = price_trend['year'].values # Extract years and prices as NumPy arrays to use them in modeling
prices = price_trend['price_per_m2'].values

# Only fit model if we have more than one data point
if len(years) > 1:
    # Fit a straight line to model the price trend over time using np.polyfit() ~ (y = mx + b --- linear regression // 1st-degree polynomial)
    coef = np.polyfit(years, prices, 1)

    # Create a function based on the fitted line to predict future prices
    trend_func = np.poly1d(coef) 

    # Predict prices for 2025 and 2026 using the model
    future_years = np.array([2025, 2026])
    future_prices = trend_func(future_years)

    # Create a DataFrame for predicted values so we can combine them with historical data
    future_df = pd.DataFrame({
        "year": future_years,
        "price_per_m2": future_prices
    })

    # Concatenate the past and predicted data using pd.concat() to create one full timeline
    full_trend = pd.concat([price_trend, future_df])

    # --- Step 5: Plot the trend using matplotlib and show it in Streamlit ---

    st.markdown(f"##### Price per m² -  {selected_district}") # use formatted string literal to combine string & variables

    # Line plot setup
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(full_trend['year'], full_trend['price_per_m2'], marker='o', linestyle='-', color='#4CAF50')  # Plot prices over years
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Price per m² (CHF)")
    ax.grid(True)
    st.pyplot(fig)

    # --- Step 6: Show predictions as success messages ---

    st.success(f"✅ Predicted price per m² for 2025: CHF {future_prices[0]:,.0f}")  # Converting a number like 8123.567 into: 8,124)
    st.success(f"✅ Predicted price per m² for 2026: CHF {future_prices[1]:,.0f}")

else:
    st.warning("Not enough data to predict trends for this district.")

# --- Footer ---

st.markdown("---")
st.caption("© 2025 - Zurich Real Estate Trends Project.")
