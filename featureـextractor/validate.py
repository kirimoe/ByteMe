import pandas

from main import extract_pe_features

df1 = pandas.read_csv('/root/ByteMe/datasets/1/PE_Header.csv')
df2 = pandas.read_csv('/root/ByteMe/datasets/1/PE_Section.csv')

df = pandas.merge(df1, df2, on='SHA256', how='inner')

bin_path = '/root/ali/files/a0afc068c4c03cbf7bcebb5d1207fd00079d4cf91dd226ab578a09ff11364998.exe'
# extract file name
file_hash= bin_path.split('/')[-1][:-4]
features = extract_pe_features(bin_path)
original_features = df[df['SHA256'] == file_hash]

print(f"Validating for {file_hash}")
print("=== Validation started ===")
# Validate keys only
for key in features.keys():
    if key not in original_features.keys():
        print(f'Key {key} not found in original features')
    
print("=== Validation  1/3 complete ===")

for key in original_features.keys():
    if key not in features.keys():
        print(f'Key {key} not found in extracted features')

print("=== Validation  2/3 complete ===")

# Validate values
for key in features.keys():

    if features[key] != original_features[key].values[0]:
        print(f'Value for key {key} does not match')
        print(f'Original: {original_features[key].values[0]}')
        print(f'Extracted: {features[key]}')
        print("===")

for key in original_features.keys():
    if key in ("SHA256", "Type", "Type_x", "Type_y"):
        continue
    
    if features[key] != original_features[key].values[0]:
        print(f'Value for key {key} does not match')
        print(f'Original: {original_features[key].values[0]}')
        print(f'Extracted: {features[key]}')
        print("===")

print("=== Validation  3/3 complete ===")