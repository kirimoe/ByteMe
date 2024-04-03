import csv

# Open the CSV file
with open('../datasets/1/PE_Section.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)
    
    # Initialize a counter
    row_count = 0
    
    # Iterate through the rows
    for row in reader:
        # Print the first two rows
        if row_count < 1:
            print(row)
            row_count += 1
        else:
            break
