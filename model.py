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
 
def evaluate(model, horizon):
    cv = cross_validation(model, horizon=horizon)
    p = performance_metrics(cv)
    return p

def model_and_forecast(df, col):
    m = Prophet()
    train = pd.DataFrame()
    train['ds'] = df.ds
    train['y'] = df[col]
    m.fit(train)
    future = m.make_future_dataframe(periods=14)
    forecast = m.predict(future)
    p = evaluate(m, '37 days')
    model = {'train': train, 'model': m, 'forecast': forecast, 'performance': p}
    return model

def model_each_col(df):
    model_dict = {}
    df = prep_for_prophet(df)
    for col in df.drop(columns='ds'):
        model_dict[col] = model_and_forecast(df, col)
    return model_dict

# models = model_each_col(activity)

def plot_from_dict(model_dict, col):
    ref = model_dict[col]
    m = ref['model']
    forecast = ref['forecast']
    m.plot(forecast)
    plt.ylabel(col)
    plt.xlabel('date')
    plt.show()

def plot_components(model_dict, col):
    ref = model_dict[col]
    m = ref['model']
    forecast = ref['forecast']
    m.plot_components(forecast)
    plt.show()

def plot_all(model_dict, components=False):
    if components:
       for col in model_dict:
           plot_components(model_dict, col)
    else:
        for col in model_dict:
            plot_from_dict(model_dict, col)

def print_evals(model_dict):
    for model in model_dict:
        print(model)
        performance = model_dict[model]['performance']
        print(performance[['mse', 'rmse']].mean())

def predict_2wks_to_csv(model_dict):
    output = pd.DataFrame()
    for col in model_dict:
        yhat = model_dict[col]['forecast']['yhat']
        output[col] = yhat.iloc[-14:]
    output.to_csv('predictions.csv')