import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris

import sys

# CHANGE THIS TO CORRECT FOLDER NAME
dir = os.path.dirname(os.path.abspath(__file__))
HEART_PATH = os.path.join (dir, '..', '..', 'datasets')

def remove_rows_with_missing_values(data):
    df = data.copy().apply (pd.to_numeric, errors='coerce')
    return df.dropna()

def load_heart_disease_data(filenames):
    dataframes = []
    # print(HEART_PATH)
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

def get_attrs_as_matrix(args, keys, default=None):
    matrix_row = []
    
    for value in keys:
        if value in args: 
            matrix_row.append(float(args[value]))
        else:
            matrix_row.append(default)
    print(matrix_row)
    return [matrix_row]

def get_inputs_as_matrix(args, keys, default=None):
    inputs = get_inputs(args, keys)
    for key, value in inputs.items():    
        inputs[key] = float(value)

    return get_attrs_as_matrix(inputs, keys, default)
    

def train_model():
    # Loads data
    heart = load_heart_disease_data([
        "cleveland.csv",
        "switzerland.csv",
        "hungarian.csv",
        # "longbeach.csv"
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
    #ExtraTreesClassifier
    #model = ExtraTreesClassifier()
    #model.fit(train_set, train_labels)

    #LogisticRegression
    model = LogisticRegression(max_iter=10000000)
    model.fit(train_set.values, train_labels.values)

    return model

# WHAT IS attrs ??
def predict(attrs):
    model = train_model()

    return predict_with_model(attrs, model)


def predict_with_model(attrs, model):
    keys = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]
    inputs = get_attrs_as_matrix(attrs, keys, 0)
    
    return model.predict(inputs)

def main():
    # Loads data
    heart = load_heart_disease_data([
        "cleveland.csv",
        "switzerland.csv",
        "hungarian.csv",
        # "longbeach.csv"
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
    #ExtraTreesClassifier
    #model = ExtraTreesClassifier()
    #model.fit(train_set, train_labels)

    #LogisticRegression
    model = LogisticRegression(max_iter=10000000)
    model.fit(train_set.values, train_labels.values)
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

if __name__ == '__main__':
    main()
