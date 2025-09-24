import pandas as pd
import matplotlib.pyplot as plt

# Post-ACE 2025 dataset
POST_FILE = "MTA Bus Speeds 2025 Post-ACE.csv"
TARGET_ROUTES = ["B41", "BX28", "M101", "Q44+"]

# Define consistent colors for each route
ROUTE_COLORS = {
    "B41": "#1f77b4",
    "BX28": "#ff7f0e",
    "M101": "#2ca02c",
    "Q44+": "#d62728"
}

# Load dataset
df = pd.read_csv(POST_FILE)

# Filter only selected routes
df = df[df['Route ID'].isin(TARGET_ROUTES)].copy()

# Convert Average Road Speed to numeric
df['Average Road Speed'] = pd.to_numeric(df['Average Road Speed'], errors='coerce')
df = df.dropna(subset=['Average Road Speed'])

# Aggregate monthly average speeds per route using the numeric Month column
monthly_avg = df.groupby(['Month', 'Route ID'])['Average Road Speed'].mean().reset_index()
monthly_avg = monthly_avg.rename(columns={'Route ID': 'route', 'Average Road Speed': 'avg_speed_mph'})

# Pivot for plotting
pivot = monthly_avg.pivot(index='Month', columns='route', values='avg_speed_mph').sort_index()

# Reindex to ensure all months 1–12 are present
pivot = pivot.reindex(range(1,13))

# Month labels
month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Plot monthly average speeds
plt.figure(figsize=(14,6))
for route in TARGET_ROUTES:
    if route in pivot.columns:
        plt.plot(pivot.index, pivot[route], marker='o', label=route, color=ROUTE_COLORS[route], linewidth=2)

plt.title("Monthly Average Bus Speeds Post-ACE (2025)")
plt.xlabel("Month")
plt.ylabel("Average Speed (mph)")
plt.xticks(ticks=range(1,13), labels=month_labels)
plt.legend(title="Route", bbox_to_anchor=(1.02,1), loc="upper left")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
