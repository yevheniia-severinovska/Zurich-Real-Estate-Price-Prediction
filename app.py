import pandas as pd             # pandas - data handling
import streamlit as st          # streamlit - web app UI
import matplotlib.pyplot as plt # matplotlib - plotting charts
import numpy as np              # numpy - math and modeling

# Load the cleaned CSV file into a pandas DataFrame so we can easily manipulate it with pandas methods
df = pd.read_csv("clean_zurich_data.csv")

# Set the app title using Streamlit to show what the project is about
st.title("🏡 Zurich Condo Price Trends (2009–2026)")

# --- Step 1: Prepare district list for sidebar selection ---

# Custom display list with nesting to group subdistricts under each Kreis
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

# Create a map to connect display names with actual district names for filtering later
display_to_actual = {d: d for d in available_districts}

# Build the final display list and keep only valid entries from the dataset
full_display = []
for d in district_display:
    name = d.strip(" • ")                 # Remove bullet for comparison
    if name in available_districts:       # This prevents errors and improves UX by not offering choices that have no data in original cleaned table
        full_display.append(d)            # Add formatted name to sidebar list
        display_to_actual[d] = name       # So we can later match what the user selects to the real name used in the data

# Adding sidebar radio buttons to select a district from the filtered and formatted list
selected_display = st.sidebar.radio("Select District", full_display, index=0)

# Convert the selected display name back to the real name (original cleaned table) for filtering the data
selected_district = display_to_actual[selected_display]

# --- Step 2: Filter data for selected district ---

# If Zurich (Total) is selected, take all rows into account; else, filter only to selected district
if selected_district == 'Zurich (Total)':
    df_selected = df.copy()
else:
    df_selected = df[df['district'] == selected_district]

# --- Step 3: Group data by year and calculate average price per m² ---

# Use groupby().mean() to group data by year and calculate average price per m² to build a yearly trend and reset_index() to convert it back to a normal table
price_trend = df_selected.groupby("year")["price_per_m2"].mean().reset_index()

# --- Step 4: Predict price for 2025–2026 using simple linear regression ---

# Extract years and prices as NumPy arrays to use them in modeling
years = price_trend['year'].values
prices = price_trend['price_per_m2'].values

# Only fit model if we have more than one data point
if len(years) > 1:
    # Fit a straight line using np.polyfit() with degree 1 (y = mx + b --- linear regression // 1st-degree polynomial)
    coef = np.polyfit(years, prices, 1)

    # Create a function based on the fitted line to predict future prices
    trend_func = np.poly1d(coef) # np.poly1d creates a polynomial function from the model coefficients

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

    st.subheader(f"Price per m² Trend: {selected_district}") # use formatted string literal to combine string & variables

    # Create a line plot with markers and labels using matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))  # Create a wide chart (10x5 inches) for clear time-based visualization
    ax.plot(full_trend['year'], full_trend['price_per_m2'], marker='o', linestyle='-', color='#4CAF50')  # Plot prices over years
    ax.set_xlabel("Year")  # Label x-axis
    ax.set_ylabel("Average Price per m² (CHF)")  # Label y-axis
    ax.grid(True)  # Show grid for readability
    st.pyplot(fig)  # Display chart in Streamlit

    # --- Step 6: Show predictions as success messages ---

    # Format numbers with thousands separator and no decimals. (Turning a number like 8123.567 into: 8,124)
    st.success(f"✅ Predicted price per m² for 2025: CHF {future_prices[0]:,.0f}")
    st.success(f"✅ Predicted price per m² for 2026: CHF {future_prices[1]:,.0f}")

else:
    # Show warning if not enough data points for prediction
    st.warning("Not enough data to predict trends for this district.")

# --- Footer ---

# Add horizontal line and small caption for visual finish
st.markdown("---")
st.caption("© 2025 - Zurich Real Estate Trends Project.")
