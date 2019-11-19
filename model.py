import pandas as pd
import numpy as np
from sklearn import metrics
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from fbprophet import Prophet
from split import split
from acquire import get_activity
from prepare import prep_activity

def evaluate(target, train, test):
    mse = metrics.mean_squared_error(test[target], yhat[target])
    rmse = math.sqrt(mse)
    return rmse

activity = prep_activity(get_activity())

activity = activity.drop(columns=['bmr', 'time'])