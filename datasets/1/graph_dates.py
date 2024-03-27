import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('hash_dates.csv')

# Convert the "Date" column to datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Group the data by date and count the number of hashes for each date
hash_counts = df.groupby('Date').size()

# Plot the data
plt.figure(figsize=(10, 6))
hash_counts.plot(kind='line', marker='o', color='b', linestyle='-')
plt.title('Number of Hashes Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Hashes')
plt.grid(True)
plt.tight_layout()
plt.show()
