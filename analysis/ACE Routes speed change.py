import pandas as pd
import matplotlib.pyplot as plt

# Pre-ACE dataset
PRE_FILE = "MTA Bus Speeds Pre-ACE.csv"
TARGET_ROUTES = ["B41", "BX28", "M101", "Q44+"]

# Load dataset
df = pd.read_csv(PRE_FILE)

# Filter only selected routes
df = df[df['route_id'].isin(TARGET_ROUTES)].copy()

# Convert month to datetime
df['month'] = pd.to_datetime(df['month'], errors='coerce')
df = df.dropna(subset=['month'])

# Extract month timestamp for monthly aggregation
df['month_ym'] = df['month'].dt.to_period('M').dt.to_timestamp()

# Convert average_speed to numeric
df['average_speed'] = pd.to_numeric(df['average_speed'], errors='coerce')
df = df.dropna(subset=['average_speed'])

# Aggregate monthly average speeds per route
monthly_avg = df.groupby(['month_ym', 'route_id'])['average_speed'].mean().reset_index()
monthly_avg = monthly_avg.rename(columns={'route_id': 'route', 'average_speed': 'avg_speed_mph'})

# Pivot for plotting
pivot = monthly_avg.pivot(index='month_ym', columns='route', values='avg_speed_mph').sort_index()

# Plot time-series
plt.figure(figsize=(14,6))
for route in TARGET_ROUTES:
    if route in pivot.columns:
        plt.plot(pivot.index, pivot[route], marker='o', label=route)
plt.title("Yearly Average Bus Speeds Pre-ACE")
plt.xlabel("Years")
plt.ylabel("Average Speed (mph)")
plt.legend(title="Route", bbox_to_anchor=(1.02,1), loc="upper left")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
