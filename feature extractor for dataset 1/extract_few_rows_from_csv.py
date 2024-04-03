import pandas as pd

# Load a few rows from the first CSV file
df1 = pd.read_csv('../datasets/1/PE_Header.csv', nrows=1)

# Load a few rows from the second CSV file
df2 = pd.read_csv('../datasets/1/PE_Section.csv', nrows=1)

# Combine the features horizontally
combined_df = pd.concat([df1, df2], axis=1)

# Print the combined features in key-value format
print("Combined features in key-value format:")
for index, row in combined_df.iterrows():
    print(f"Row {index + 1}:")
    for column, value in row.items():
        print(f"{column}: {value}")
