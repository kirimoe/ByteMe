import _pickle as cPickle 
import gzip
from pe_extractor import PEAttributeExtractor  # Import your feature extractor function
from nfs_model import NeedForSpeedModel  # Assuming this is your NeedForSpeedModel class

def query_model(model_path, pe_file_paths, threshold):
    # Load the pretrained model from the .pkl file
    with open(model_path, 'rb') as f:
        #fp = gzip.open(model_path,'rb')
        model = cPickle.load(f)
    # Iterate through each PE file
    for file_path in pe_file_paths:
        # Read the PE file
        with open(file_path, 'rb') as f:
            bytez = f.read()

        try:
            # Extract features from the PE file using your feature extractor
            print("hello")
            features = PEAttributeExtractor(bytez)  # Implement this function in your feature extractor file
            # Make predictions using the loaded model
            result = model.predict_threshold(features.reshape(1, -1), threshold)[0]
            print(f"File: {file_path}, Prediction: {'Malicious' if result == 1 else 'Not Malicious'}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    model_path = 'NFS_21_ALL_hash_50000_WITH_MLSEC20.pkl'  # Path to your pretrained model .pkl file
    pe_file_paths = ['CFFLAT.exe']  # List of PE file paths
    threshold = 0.8  # Threshold for making predictions

    query_model(model_path, pe_file_paths, threshold)
