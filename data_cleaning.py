import pandas as pd

# 1. Загрузить файл
df = pd.read_csv("zurich-condos.csv")  # Убедись, что файл лежит в той же папке

# 2. Переименовать ВСЕ нужные колонки с немецкого на английский
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

# ✅ 2.5 Заменить "Ganze Stadt" на более понятное название
df["district"] = df["district"].replace({"Ganze Stadt": "Zurich (Total)"})

# 3. Привести нужные столбцы к типу float
df["median_price"] = pd.to_numeric(df["median_price"], errors='coerce')
df["price_per_m2"] = pd.to_numeric(df["price_per_m2"], errors='coerce')
df["total_price"] = pd.to_numeric(df["total_price"], errors='coerce')

# 4. Извлечь минимальное значение из диапазона в колонке num_units
df["num_units_clean"] = (
    df["num_units"]
    .astype(str)
    .str.replace("-", "–")  # Replace short hyphen with long dash
    .str.split("–")
    .str[0]
    .astype(float)
)

# 5. Убрать плохие строки:
df_clean = df[
    (df["median_price"] > 0) &
    (df["price_per_m2"] > 0) &
    (df["total_price"] > 0) &
    (df["num_units_clean"] >= 3)
].copy()

# 6. Сохранить очищенный датасет
df_clean.to_csv("clean_zurich_data.csv", index=False)

print("✅ Data cleaned, renamed, types fixed, and saved successfully!")
