# ============================================================================
# SECTION 1: Load and Explore the Dataset
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('data/real_state_ecuador_dataset.csv')

print("Dataset Shape:", df.shape)
print("\n" + "="*80)
print("Column Names and Data Types:")
print("="*80)
print(df.dtypes)
print("\n" + "="*80)
print("First few rows:")
print("="*80)
print(df.head())
print("\n" + "="*80)
print("Dataset Info:")
print("="*80)
print(df.info())

# ============================================================================
# SECTION 2: Data Cleaning and Normalization
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: Data Cleaning and Normalization")
print("="*80)

# Clean Lugar column - extract the main location (usually the city/neighborhood)
def normalize_lugar(lugar_str):
    if pd.isna(lugar_str):
        return np.nan
    
    # Remove extra whitespace
    lugar_str = str(lugar_str).strip()
    
    # Split by comma and take the second element (usually the city/neighborhood)
    parts = [p.strip() for p in lugar_str.split(',')]
    
    if len(parts) > 1:
        # Return the second part (more specific location)
        return parts[1]
    else:
        # If just one part, return it
        return parts[0]

df['Lugar_Normalizado'] = df['Lugar'].apply(normalize_lugar)

print("Sample normalized locations:")
print(df[['Lugar', 'Lugar_Normalizado']].drop_duplicates().head(20))

# ============================================================================
# SECTION 3: Handle Missing Values
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: Handle Missing Values")
print("="*80)

# Check missing values
print("\nMissing values by column:")
print(df.isnull().sum())
print("\nMissing values percentage:")
print((df.isnull().sum() / len(df) * 100).round(2))

# For properties with multiple uses (commercial, offices), missing values in 
# dormitorios, banos, garages are common. We'll handle them:
# Strategy: Drop rows with missing Precio or Lugar
# For dormitorios, banos, garages: fill with median by Provincia

df_clean = df.dropna(subset=['Precio', 'Lugar_Normalizado', 'Area']).copy()

# Convert numeric columns to numeric type (handle any string values)
numeric_cols = ['Num. dormitorios', 'Num. banos', 'Num. garages', 'Area', 'Precio']
for col in numeric_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Fill missing values with median by Provincia
for col in ['Num. dormitorios', 'Num. banos', 'Num. garages']:
    df_clean[col] = df_clean.groupby('Provincia')[col].transform(
        lambda x: x.fillna(x.median())
    )

# For any remaining NaN, fill with overall median
df_clean[['Num. dormitorios', 'Num. banos', 'Num. garages']] = df_clean[
    ['Num. dormitorios', 'Num. banos', 'Num. garages']
].fillna(df_clean[['Num. dormitorios', 'Num. banos', 'Num. garages']].median())

print(f"\nDataset shape after cleaning: {df_clean.shape}")
print("\nMissing values after cleaning:")
print(df_clean.isnull().sum())

# ============================================================================
# SECTION 4: Descriptive Analysis
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: Descriptive Analysis")
print("="*80)

# Total properties
print(f"\nTotal properties in dataset: {len(df_clean)}")

# Properties by Provincia
print("\nProperties by Provincia:")
print(df_clean['Provincia'].value_counts().sort_values(ascending=False))

# Properties by Lugar
print("\n" + "="*50)
print("Top 20 properties by Location (Lugar):")
print("="*50)
print(df_clean['Lugar_Normalizado'].value_counts().head(20))

# Price statistics (general)
print("\n" + "="*50)
print("Price Statistics (General):")
print("="*50)
print(f"Mean Price: ${df_clean['Precio'].mean():.2f}")
print(f"Median Price: ${df_clean['Precio'].median():.2f}")
print(f"Std Dev: ${df_clean['Precio'].std():.2f}")
print(f"Min Price: ${df_clean['Precio'].min():.2f}")
print(f"Max Price: ${df_clean['Precio'].max():.2f}")

# Price statistics by Lugar
print("\n" + "="*50)
print("Price Statistics by Top 10 Locations:")
print("="*50)
top_lugares = df_clean['Lugar_Normalizado'].value_counts().head(10).index
precio_by_lugar = df_clean[df_clean['Lugar_Normalizado'].isin(top_lugares)].groupby(
    'Lugar_Normalizado'
)['Precio'].agg(['count', 'mean', 'median', 'std']).round(2)
print(precio_by_lugar)

# Relationship between Area and Price
print("\n" + "="*50)
print("Relationship between Area and Price:")
print("="*50)
correlation = df_clean['Area'].corr(df_clean['Precio'])
print(f"Correlation between Area and Price: {correlation:.4f}")

# Premium by Room Additions
print("\n" + "="*50)
print("Premium by Additional Bedroom:")
print("="*50)

# Calculate average price by number of bedrooms
price_by_bedrooms = df_clean.groupby('Num. dormitorios')['Precio'].agg(['count', 'mean']).round(2)
print(price_by_bedrooms)

print("\nPremium Analysis (comparing consecutive bedroom counts):")
bedrooms_sorted = sorted(df_clean['Num. dormitorios'].unique())
for i in range(len(bedrooms_sorted) - 1):
    br1 = bedrooms_sorted[i]
    br2 = bedrooms_sorted[i + 1]
    
    price_br1 = df_clean[df_clean['Num. dormitorios'] == br1]['Precio'].mean()
    price_br2 = df_clean[df_clean['Num. dormitorios'] == br2]['Precio'].mean()
    premium = price_br2 - price_br1
    
    print(f"{int(br1)} → {int(br2)} bedrooms: ${premium:.2f} premium ({(premium/price_br1*100):.1f}%)")

# ============================================================================
# SECTION 5: Create Price Category Column
# ============================================================================
print("\n" + "="*80)
print("SECTION 5: Create Price Category Column")
print("="*80)

def categorize_price_by_lugar(df):
    """Create price categories based on quartiles per location"""
    df_copy = df.copy()
    df_copy['Tipo_Precio'] = 'Medio'  # Default
    
    # Get unique locations
    locations = df_copy['Lugar_Normalizado'].unique()
    
    for loc in locations:
        # Calculate quartiles for this location
        loc_mask = df_copy['Lugar_Normalizado'] == loc
        q1 = df_copy[loc_mask]['Precio'].quantile(0.25)
        q3 = df_copy[loc_mask]['Precio'].quantile(0.75)
        
        # Assign categories
        df_copy.loc[(loc_mask) & (df_copy['Precio'] < q1), 'Tipo_Precio'] = 'Económico'
        df_copy.loc[(loc_mask) & (df_copy['Precio'] > q3), 'Tipo_Precio'] = 'Lujo'
    
    return df_copy

df_clean = categorize_price_by_lugar(df_clean)

print("\nPrice Category Distribution:")
print(df_clean['Tipo_Precio'].value_counts())
print(f"\nPercentage distribution:")
print((df_clean['Tipo_Precio'].value_counts() / len(df_clean) * 100).round(2))

# Sample of each category
print("\n" + "="*50)
print("Sample properties by price category:")
print("="*50)
for category in ['Económico', 'Medio', 'Lujo']:
    sample = df_clean[df_clean['Tipo_Precio'] == category].head(2)
    print(f"\n{category}:")
    print(sample[['Precio', 'Area', 'Num. dormitorios', 'Lugar_Normalizado', 'Tipo_Precio']])

# Save the cleaned dataset
df_clean.to_csv('data/real_state_clean.csv', index=False)
print(f"\n✓ Cleaned dataset saved to 'data/real_state_clean.csv'")
