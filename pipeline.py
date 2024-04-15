
from featureـextractor import extract_features_1, extract_features_2
from packer_cryptor_detect.detector import analyze_file

from keras.models import load_model
import numpy as np
import gzip
import _pickle as cPickle
from joblib import load

import pandas as pd

def load_gzip_pickle(filename):
    fp = gzip.open(filename, 'rb')
    obj = cPickle.load(fp)
    fp.close()
    return obj

def get_rf_prediction(features):
    # load rf_classifier from disk
    rf_classifier = load("./models/rf_classifier.joblib")
    y_pred_proba = rf_classifier.predict_proba([features])[:, 1]
    threshold = 0.8
    y_pred = (y_pred_proba >= threshold).astype(int)
    if len(y_pred) == 1:
        return y_pred[0]
    else:
        return 0


def get_dt_prediction(features):
    # load dt_classifier from disk
    dt_classifier = load("./models/dt_classifier.joblib")
    y_pred_proba = dt_classifier.predict_proba([features])[:, 1]
    threshold = 0.9
    y_pred = (y_pred_proba >= threshold).astype(int)
    if len(y_pred) == 1:
        return y_pred[0]
    else:
        return 0


def get_gb_prediction(features):
    # load gb_classifier from disk
    gb_classifier = load("./models/gb_classifier.joblib")
    y_pred_proba = gb_classifier.predict_proba([features])[:, 1]
    threshold = 0.9
    y_pred = (y_pred_proba >= threshold).astype(int)
    if len(y_pred) == 1:
        return y_pred[0]
    else:
        return 0


def get_keras_prediction(features):
    scaler = load("./models/scaler.save")
    model = load_model("./models/keras_model.keras")
    sample = np.array(features)
    sample_scaled = scaler.transform(sample.reshape(1, -1))
    threshold = 0.85
    y_pred_proba = model.predict(sample_scaled)
    y_pred = 1 if y_pred_proba >= threshold else 0
    return y_pred


def get_ember_prediction(features):
    ember_classifier = load_gzip_pickle("./models/ember_model.pkl")
    f = pd.DataFrame([features])
    threshold = 0.75
    y_pred = ember_classifier.predict_threshold(f, threshold=threshold)
    if len(y_pred) == 1:
        return y_pred[0]
    else:
        return 0


    

def get_votes(filepath: str):
    votes = []
    
    features_1 = extract_features_1(filepath)
    features_2 = extract_features_2(filepath)

    rf = get_rf_prediction(features_1)
    dt = get_dt_prediction(features_1)
    gb = get_gb_prediction(features_1)
    kr = get_keras_prediction(features_1)
    em = get_ember_prediction(features_2)
    
    packers = analyze_file(filepath)
    
    votes.append(rf)
    votes.append(dt)
    votes.append(gb)
    votes.append(kr)
    votes.append(em)
    votes.append(packers)
    
    return votes


if __name__ == "__main__":
    goodware = "/root/ali/goodwares/fff32ccd4f6dfdde4c80710074fa78dda53f1aaeaa67c1936a61e38270efa437.exe"
    malware = "/root/ali/malwares/00000fa1585e99fcb5e8728b96f173ff61b08fc152e2f50d715f6d596dec42fb.exe" 
    get_votes(malware)
