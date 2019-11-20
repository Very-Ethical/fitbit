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

caps_and_floors = {'steps': {'floor': 0, 'cap': 25000},
                   'total_burned': {'floor': 799, 'cap': 5000},
                   'distance': {'floor': 0, 'cap': 11},
                   'floors': {'floor': 0, 'cap': 30},
                   'out': {'floor': 28, 'cap': 1400},
                   'fat_burn': {'floor': 0, 'cap': 350},
                   'cardio': {'floor': 0, 'cap': 80},
                   'peak': {'floor': 0, 'cap': 160},
                   'active_burned': {'floor': 0, 'cap': 2000}}
 
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
    plt.ylabel(col)
    plt.xlabel('date')
    plt.show()

def plot_all(caps_and_floors):
    for col in caps_and_floors:
        plot_from_dict(caps_and_floors, col)

def evaluate(caps_and_floors, col, test):
    y = test[col]
    yhat = caps_and_floors[col]['model']['forecast']['yhat']
    yhat = yhat.iloc[-37:]
    mse = metrics.mean_squared_error(y, yhat)
    rmse = mse ** 1/2
    return mse, rmse

def evaluate_all(caps_and_floors, test):
    results = {}
    for col in caps_and_floors:
        raw = evaluate(caps_and_floors, col, test)
        results[col] = {'mse': raw[0], 'rmse': raw[1]}
    return results

predictive = {'steps': {'floor': 0, 'cap': 25000},
              'total_burned': {'floor': 799, 'cap': 5000},
              'distance': {'floor': 0, 'cap': 11},
              'floors': {'floor': 0, 'cap': 30},
              'out': {'floor': 28, 'cap': 1400},
              'fat_burn': {'floor': 0, 'cap': 350},
              'cardio': {'floor': 0, 'cap': 80},
              'peak': {'floor': 0, 'cap': 160},
              'active_burned': {'floor': 0, 'cap': 2000}}

def predict_2wks_to_csv(df, caps_and_floors):
    df = prep_for_prophet(df)
    model_each_col(df, caps_and_floors)
    output = pd.DataFrame()
    for col in caps_and_floors:
        yhat = caps_and_floors[col]['model']['forecast']['yhat']
        output[col] = yhat
    output.to_csv('predictions.csv')