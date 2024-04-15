import pandas as pd
import gzip

import _pickle as cPickle

import pickle

from ember_model import NeedForSpeedModel, RandomForestClassifier


def save_gzip_pickle(filename, obj):
    fp = gzip.open(filename, 'wb')
    cPickle.dump(obj, fp)
    fp.close()

# read pkl file
with open("ember_train_data.pkl", 'rb') as f:
    train_attributes = pickle.load(f)
train_data_path = "/root/ByteMe/models/ember_train_data.csv"
train_data = pd.DataFrame(train_attributes)


clf = NeedForSpeedModel(classifier=RandomForestClassifier(n_jobs=-1))
clf.fit(train_data)
# save model
save_gzip_pickle("ember_model.pkl", clf)
