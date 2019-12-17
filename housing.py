import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier

HOUSING_PATH = os.path.join ("datasets", "housing")

def load_housing_data():
    csv_path = os.path.join(HOUSING_PATH, "housing.csv")
    return pd.read_csv(csv_path)

housing = load_housing_data()

train_set, test_set = train_test_split(housing, test_size=.2, random_state=42)

# def split_train_test(data, ratio):
#     total_len = len(data)
#     shuffled = np.random.permutation(total_len) #randomiza
#     shuffled = np.random.seed(42) #randomiza
#     size = int(total_len * ratio)
#     test_indexes = shuffled[:size]
#     train_indexes = shuffled[size:]
#     return data.iloc[train_indexes], data.iloc[test_indexes] #



# model = ExtraTreesClassifier()

# model.fit(train_set, train_labels)
# result = model.score(test_set, test_labels)

# print("Acuracia", result)