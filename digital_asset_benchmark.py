import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Sets display options to show all columns and rows for easier viewing
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# PART 1: Generate Mock "Messy" Data
def generate_mock_data(n=150):
    firm_types = ['Asset Manager', 'Custodian Bank', 'Broker-Dealer', 'Hedge Fund']
    regions = ['North America', 'APAC', 'EMEA']
    barriers = ['Legacy Technology', 'Regulatory Uncertainty', 'Talent Shortage', 'Budget Constraints']
    stages = ['Not Started', 'Researching', 'POC Phase', 'Live Production']
    
    data = []
    for _ in range(n):
        # Simulates a mix of Clean numbers and Messy Strings to test auditing logic
        # 30% chance of a clean number (e.g., 500000000)
        # 70% chance of messy data (e.g., "$500M" or NaN)
        is_clean = random.random() < 0.3
        
        if is_clean:
            # Generate a raw number (Clean)
            aum_raw = random.randint(10_000_000, 500_000_000_000)
        else:
            # Generate messy string or missing value
            aum_raw = random.choice([f"${random.randint(1, 500)}B", f"{random.randint(100, 900)}M", np.nan])
        
        row = {
            "Firm ID": f"VX-{random.randint(1000, 9999)}",
            "Firm Type": random.choices(firm_types, weights=[0.4, 0.2, 0.3, 0.1])[0],
            "Region": random.choice(regions),
            "AUM (Raw)": aum_raw,
            "Digital Asset Strategy": random.choices(stages, weights=[0.2, 0.3, 0.4, 0.1])[0],
            "Top Barrier": random.choice(barriers),
            "Satisfaction Score": random.randint(1, 10)
        }
        data.append(row)
    
    return pd.DataFrame(data)

# Generate and display raw data sample
df_raw = generate_mock_data()
print("-- Raw Data Sample (Messy data) --")
print(df_raw.head())

# -- PART 2: Data Cleaning & Structuring --

# Tracks if a row needed normalization
def needs_normalization(value):
    # Needs normalization if it is a String (has '$' or 'B') or is NaN (Missing)
    if pd.isna(value):
        return True
    if isinstance(value, str):
        return True
    return False

# Counts the messy rows before we fix them
messy_rows_count = df_raw['AUM (Raw)'].apply(needs_normalization).sum()
total_rows = len(df_raw)
normalization_percentage = (messy_rows_count / total_rows) * 100

def clean_aum(value):
    """Parses strings to floats, fills NaNs, leaves integers alone."""
    if pd.isna(value):
        return 0
    if isinstance(value, (int, float)):
        return value
    # String parsing logic
    value = str(value).replace('$', '').replace(' ', '')
    if 'B' in value:
        return float(value.replace('B', '')) * 1_000_000_000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1_000_000
    return 0

df_clean = df_raw.copy()
df_clean['AUM (Numeric)'] = df_clean['AUM (Raw)'].apply(clean_aum)
df_clean['AUM (Billions)'] = df_clean['AUM (Numeric)'] / 1_000_000_000

# Categorizes firms by size of AUM
df_clean['Size Cohort'] = pd.cut(df_clean['AUM (Billions)'], 
                                 bins=[-1, 10, 100, 10000], 
                                 labels=['Small (<$10B)', 'Mid-Tier ($10-100B)', 'Large (>$100B)'])

print("\n-- Clean Data Sample --")
print(df_clean[['Firm Type', 'AUM (Raw)', 'AUM (Billions)', 'Size Cohort']].head())

# -- PART 3: Generate Insights (Visualization) --
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

# Chart 1: Barriers by Firm Type
plt.figure(figsize=(10, 6))
barrier_counts = df_clean.groupby(['Firm Type', 'Top Barrier']).size().unstack(fill_value=0)
barrier_pct = barrier_counts.div(barrier_counts.sum(axis=1), axis=0) * 100

barrier_pct.plot(kind='barh', stacked=True, colormap='viridis', figsize=(10, 6))
plt.title('Primary Barriers to Digital Asset Adoption by Firm Type', fontsize=14, fontweight='bold')
plt.xlabel('Percentage of Respondents')
plt.ylabel('')
plt.legend(title='Barrier', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('chart_1_barriers.png')
print("\n[Generated] chart_1_barriers.png")

# Chart 2: Adoption Stage by Region
plt.figure(figsize=(8, 6))
sns.countplot(data=df_clean, x='Region', hue='Digital Asset Strategy', palette='Blues')
plt.title('Regional Benchmarking: Digital Asset Maturity', fontsize=14, fontweight='bold')
plt.ylabel('Number of Firms')
plt.tight_layout()
plt.savefig('chart_2_regional_readiness.png')
print("[Generated] chart_2_regional_readiness.png")

# -- PART 4: Automated Key Findings --
pct_legacy = len(df_clean[df_clean['Top Barrier'] == 'Legacy Technology']) / len(df_clean) * 100
leading_region = df_clean[df_clean['Digital Asset Strategy'] == 'Live Production']['Region'].mode()[0]

print("\n-- Automated Executive Summary --")
print(f"1. Legacy Technology is the primary blocker for {pct_legacy:.1f}% of respondents, indicating a critical need for infrastructure modernization before digital asset integration.")
print(f"2. {leading_region} is currently leading the 'Live Production' phase, outperforming other regions in operational readiness.")
print(f"3. Data Quality Audit: {normalization_percentage:.1f}% of input records required automated normalization to be usable for analysis.")