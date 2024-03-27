import glob
import csv
import json

directory_path = '.'
csv_files = glob.glob(directory_path + '/*.csv')
hashes = set()

for file_path in csv_files:
    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        # skip header
        next(csv_reader)
        for row in csv_reader:
            hash_value = row[0]
            hashes.add(hash_value)

print(f"Length of hashes: {len(hashes)}")
# save the hashes to a json list
hashes_list = list(hashes)
with open('hashes.json', 'w') as file:
    file.write(json.dumps(hashes_list, indent=2))
