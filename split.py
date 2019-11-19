import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from acquire import get_activity
from prepare import prep_activity

activity = prep_activity(get_activity())

activity = activity.reset_index()

def split(df, y, x='date'):
    tss = TimeSeriesSplit(5)
    for train_index, test_index in tss.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
    X_train = train[x]
    y_train = train[y]
    X_test = test[x]
    y_test = test[y]
    return X_train, y_train, X_test, y_test