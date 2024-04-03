import pandas as pd

# Load the first row of the first CSV file into a DataFrame
df1_columns = pd.read_csv('../datasets/1/PE_Header.csv', nrows=1)

# Load the first row of the second CSV file into another DataFrame
df2_columns = pd.read_csv('../datasets/1/PE_Section.csv', nrows=1)

combined_columns = list(set(df1_columns) | set(df2_columns))

# Print the distinct column names
print("Distinct feature names:")
print(combined_columns)
