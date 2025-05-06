import pandas as pd

# --- Step 1: Loading the file
df = pd.read_csv("zurich-condos.csv")  

# --- Step 2: GE -> EN 
rename_dict = {
    "Stichtagdatjahr": "year",
    "DatenstandCd": "data_status_code",
    "HAArtLevel1Sort": "property_type_sort",
    "HAArtLevel1Cd": "property_type_code",
    "HAArtLevel1Lang": "property_type",
    "HASTWESort": "market_segment_sort",
    "HASTWECd": "market_segment_code",
    "HASTWELang": "market_segment",
    "RaumSort": "district_sort",
    "RaumCd": "district_code",
    "RaumLang": "district",
    "AnzHA": "num_units",
    "HAPreisWohnflaeche": "price_per_m2",
    "HAMedianPreis": "median_price",
    "HASumPreis": "total_price"
}
df.rename(columns=rename_dict, inplace=True)

df["district"] = df["district"].replace({"Ganze Stadt": "Zurich (Total)"})

# --- Step 3: Columns into float type
df["median_price"] = pd.to_numeric(df["median_price"], errors='coerce')
df["price_per_m2"] = pd.to_numeric(df["price_per_m2"], errors='coerce')
df["total_price"] = pd.to_numeric(df["total_price"], errors='coerce')

# --- Step 4: Bring column num_units to min value
df["num_units_clean"] = (
    df["num_units"]
    .astype(str)
    .str.replace("-", "–")
    .str.split("–")
    .str[0]
    .astype(float)
)

# --- Step 5: Remove irrevevant lines
df_clean = df[
    (df["median_price"] > 0) &
    (df["price_per_m2"] > 0) &
    (df["total_price"] > 0) &
    (df["num_units_clean"] >= 3)
].copy()

# --- Step 6: Save cleaned csv
df_clean.to_csv("clean_zurich_data.csv", index=False)

print("✅ Data cleaned, renamed, types fixed, and saved successfully!")
