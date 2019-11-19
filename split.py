import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from acquire import get_activity
from prepare import prep_activity

activity = prep_activity(get_activity())

activity = activity.reset_index()
