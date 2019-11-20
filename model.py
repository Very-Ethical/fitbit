import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
from acquire import get_activity
from prepare import prep_activity, prep_for_prophet, split

activity = prep_activity(get_activity())
activity = activity.reset_index()
train, test = split(activity)
train = prep_for_prophet(train)
test = prep_for_prophet(test)

caps_and_floors = {'steps': {'floor': 0, 'cap': 30_000},
                   'total_burned': {'floor': 799, 'cap': 6000},
                   'distance': {'floor': 0, 'cap': 20},
                   'floors': {'floor': 0, 'cap': 250},
                   'out': {'floor': 28, 'cap': 1440},
                   'fat_burn': {'floor': 0, 'cap': 400},
                   'cardio': {'floor': 0, 'cap': 100},
                   'peak': {'floor': 0, 'cap': 200},
                   'active_burned': {'floor': 0, 'cap': 4000}}
 
def model_and_forecast(df, col, caps_and_floors):
    m = Prophet(daily_seasonality = True, growth = 'logistic', changepoint_range = 0.9)
    train = pd.DataFrame()
    train['ds'] = df.ds
    train['y'] = df[col]
    train['cap'] = caps_and_floors[col]['cap']
    train['floor'] = caps_and_floors[col]['floor']
    m.fit(train)
    future = m.make_future_dataframe(periods=37)
    future['cap'] = caps_and_floors[col]['cap']
    future['floor'] = caps_and_floors[col]['floor']
    forecast = m.predict(future)
    model = {'train': train, 'model': m, 'forecast': forecast}
    return model

def model_each_col(df, caps_and_floors):
    for col in caps_and_floors:
        caps_and_floors[col]['model'] = model_and_forecast(df, col, caps_and_floors)
    return caps_and_floors

caps_and_floors = model_each_col(train, caps_and_floors)

def plot_from_dict(caps_and_floors, col):
    ref = caps_and_floors[col]['model']
    m = ref['model']
    forecast = ref['forecast']
    m.plot(forecast)
    plt.show()

def plot_all(caps_and_floors):
    for col in caps_and_floors:
        plot_from_dict(caps_and_floors, col)

# def evaluate(caps_and_floors, col):
