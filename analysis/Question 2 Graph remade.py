import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Load dataset
df = pd.read_csv("MTA ACE Violations Dataset.csv")

# Step 4: Filter for exempt violations
df_exempt = df[df['Violation Status'].str.contains("exempt", case=False, na=False)]

# Step 5: Count violations per exempt category
exempt_counts = df_exempt['Violation Status'].value_counts()

# Step 6: Clean labels (remove 'EXEMPT - ' prefix)
labels = [s.replace('EXEMPT - ', '').strip() for s in exempt_counts.index]

# Step 7: Display counts in console
print("Exempt Violation Counts:")
for label, count in zip(labels, exempt_counts.values):
    print(f"{label}: {count}")

# Step 8: Visualize with a bar chart
plt.figure(figsize=(10,6))
plt.bar(labels, exempt_counts.values, color='skyblue', width = 0.5)
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Violations")
plt.title("Exempt Violation Counts per Category")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
