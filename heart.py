import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
import sys

# CHANGE THIS TO CORRECT FOLDER NAME
HEART_PATH = os.path.join ("datasets")

def remove_rows_with_missing_values(data):
    df = data.copy().apply (pd.to_numeric, errors='coerce')
    return df.dropna()

def load_heart_disease_data(filenames):
    dataframes = []
    for filename in filenames:    
        csv_path = os.path.join(HEART_PATH, filename)
        df = pd.read_csv(csv_path)
        dataframes.append(df)
    return pd.concat(dataframes)

def replace_with_mean(df, attribute):
    clone = df.copy()
    vals = pd.to_numeric(clone[attribute], errors='coerce')
    clone[attribute] = vals.fillna(vals.mean()) 

    return clone

def replace_with_mode(df, attribute):
    clone = df.copy()
    vals = pd.to_numeric(clone[attribute], errors='coerce')
    clone[attribute] = vals.fillna(vals.mode()) 
    
    return clone

def replace_with_value(df, attribute, value):
    clone = df.copy()
    vals = pd.to_numeric(clone[attribute], errors='coerce')
    clone[attribute] = vals.fillna(0) 
    
    return clone

def get_inputs(args, keys):
    inputs = {}

    for value in args:
        parts = value.split("=")
        if parts[0] in keys: inputs[parts[0]] = parts[1]
    
    for value in keys:
        if value not in keys: inputs[value] = None

    return inputs

def get_inputs_as_matrix(args, keys, default=None):
    matrix_row = []

    inputs = get_inputs(args, keys)

    for value in keys:
        if value in inputs: matrix_row.append(inputs[value])
        else: matrix_row.append(default)
    
    return [matrix_row]

# Loads data
heart = load_heart_disease_data([
    "cleveland.csv",
    "switzerland.csv",
    "hungarian.csv",
    "longbeach.csv"
])

# Cleans dataframe
heart = replace_with_value(heart, 'thal', 0)
heart = replace_with_mean(heart, 'ca')
heart = replace_with_mode(heart, 'fbs')
heart = remove_rows_with_missing_values(heart)

labels = heart['num']
examples = heart.drop('num', axis=1)

#Creates train and test data sets
test_size = .20
train_set, test_set, train_labels, test_labels = train_test_split(examples, labels, test_size=test_size, random_state=42)

#Creates model
model = ExtraTreesClassifier()
model.fit(train_set, train_labels)

if sys.argv[1] == 'test':
    # Test and print results
    result = model.score(test_set, test_labels)

    print("Total number of examples:", len(heart))
    print('Test size: %d' %(test_size * 100))
    print("Accuracy: ", result)
else:
    # Predict result
    keys = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]
    inputs = get_inputs_as_matrix(sys.argv, keys, 0)
    
    result = model.predict(inputs)
    print(result)