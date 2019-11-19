import pandas as pd


def get_activity():
    activity = pd.read_csv('activity.csv')
    return activity