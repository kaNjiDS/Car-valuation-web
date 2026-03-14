# processed_dataset_creator.py
import pandas as pd
import numpy as np

# ── 1. Load raw data ───────────────────────────────────────────────
df = pd.read_csv("car_price_dataset.csv", index_col=0)
print("Original shape:", df.shape)

# ── 2. Remove duplicates ───────────────────────────────────────────
df.drop_duplicates(inplace=True)

# ── 3. Remove irrelevant columns ───────────────────────────────────
df.drop('Date', axis=1, inplace=True)

# ── 4. Filter to used vehicles only ────────────────────────────────
df = df[df['Condition'] == 'USED']

# ── 5. Feature engineering: Age ────────────────────────────────────
df['Age'] = 2026 - df['YOM']

# ── 6. Rename columns for consistency ──────────────────────────────
df.rename(columns={
    'Brand': 'brand',
    'Model': 'model',
    'YOM': 'yom',
    'Engine (cc)': 'engine_cc',
    'Gear': 'transmission',
    'Fuel Type': 'fuel_type',
    'Millage(KM)': 'mileage',
    'Town': 'town',
    'Leasing': 'leasing',
    'Condition': 'condition',
    'AIR CONDITION': 'air_condition',
    'POWER STEERING': 'power_steering',
    'POWER MIRROR': 'power_mirror',
    'POWER WINDOW': 'power_window',
    'Price': 'price'
}, inplace=True)

# ── 7. Map binary comfort features ────────────────────────────────
binary_cols = ['air_condition', 'power_steering', 'power_mirror', 'power_window']
for col in binary_cols:
    df[col] = (df[col] == 'Available')

# ── 8. Log transformations for skewed variables ────────────────────
df['log_engine_cc'] = np.log(df['engine_cc'].clip(1))  # clip to avoid log(0) if any
df['price_transformed'] = np.log(df['price'].clip(1))  # assuming price in millions, clip for safety

# ── 9. Urban classification based on municipal/urban councils ──────
urban_towns = [
    'Colombo', 'Dehiwala-Mount Lavinia', 'Dehiwala-Mount-Lavinia', 'Kotte', 'Kaduwela', 'Moratuwa', 
    'Negombo', 'Gampaha', 'Kurunegala', 'Kandy', 'Matale', 'Dambulla', 'Nuwara-Eliya', 'Badulla', 
    'Bandarawela', 'Galle', 'Matara', 'Hambantota', 'Ratnapura', 'Anuradhapura', 'Polonnaruwa', 
    'Jaffna', 'Batticaloa', 'Kalmunai', 'Akkaraipattu', 'Kolonnawa', 'Maharagama', 'Boralesgamuwa', 
    'Kesbewa', 'Wattala', 'Peliyagoda', 'Katunayake', 'Minuwangoda', 'Ja-Ela', 'Panadura', 'Horana', 
    'Kalutara', 'Beruwala', 'Kuliyapitiya', 'Puttalam', 'Chilaw', 'Wattegama', 'Kadugannawa', 
    'Gampola', 'Nawalapitiya', 'Hatton', 'Haputale', 'Ambalangoda', 'Hikkaduwa', 'Weligama', 
    'Tangalle', 'Balangoda', 'Embilipitiya', 'Kegalle', 'Chavakachcheri', 'Mannar', 'Vavuniya', 
    'Kattankudy', 'Ampara', 'Trincomalee'
]  # Adjusted for data spellings
df['town_is_urban'] = df['town'].isin(urban_towns)

# ── 10. Drop unnecessary columns (e.g., condition now uniform) ─────
df.drop('condition', axis=1, inplace=True)

# ── 11. Final checks (optional: handle outliers if needed) ─────────
# From report: no unrealistic values detected, so skipping advanced outlier removal

print("Processed shape:", df.shape)
print(df.head(3))

# ── 12. Save processed version ────────────────────────────────────
df.to_csv("processed_data.csv", index=False)
print("Saved successfully!")