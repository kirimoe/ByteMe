import pickle
from pe_extractor import PEAttributeExtractor  # Assuming you have your feature extractor Python file
import pandas as pd
import joblib



#threshold = 0.75

# Load the pretrained model
#with open('NFS_21_ALL_hash_50000_WITH_MLSEC20.pkl', 'rb') as f:
#    model = pickle.load(f)

model = joblib.load('NFS_21_ALL_hash_50000_WITH_MLSEC20.pkl')

with open("CFFLAT.exe", "rb") as f:
        bytez = f.read()

pe_att_ext = PEAttributeExtractor(bytez)
atts = pe_att_ext.extract()

atts = pd.DataFrame([atts])
result = model.predict_threshold(atts, threshold)[0]
print('LABEL = ', result)