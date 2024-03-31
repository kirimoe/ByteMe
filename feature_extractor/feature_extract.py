from ember import PEFeatureExtractor
import lief, sys

def extract_features_from_file(file_path):
    # Load the PE file
    try:
        with open(file_path, 'rb') as f:
            bytez = f.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

    # Initialize the PEFeatureExtractor
    extractor = PEFeatureExtractor(feature_version=2)

    # Extract features from the PE file
    try:
        features = extractor.feature_vector(bytez)
    except lief.not_found:
        print(f"Failed to parse '{file_path}'. It may not be a valid PE file.")
        return None

    return features

def main():
    # Path to your file
    file_path = sys.argv[1]

    # Extract features from the file
    features = extract_features_from_file(file_path)

    if features is not None:
        print("Extracted features:")
        print(features)

if __name__ == "__main__":
    main()
