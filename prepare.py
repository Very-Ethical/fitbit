import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from acquire import get_activity

def commas_to_ints(df, columns):
    for col in columns:
        df[col] = df[col].str.replace(',','')
        df[col] = df[col].astype('int')
    return df

def prep_activity(df):
    # lazy, short names for lazy programmers
    lazy_names = {'Date': 'date', 'Calories Burned': 'total_burned', 'Steps': 'steps', 'Distance': 'distance',
                'Floors': 'floors', 'Minutes Sedentary': 'sedentary', 'Minutes Lightly Active': 'lightly',
                'Minutes Fairly Active': 'fairly', 'Minutes Very Active': 'very', 'Activity Calories': 'active_burned'}

    df = df.rename(columns=lazy_names)

    # change datatypes to more appropriate ones
    # date to datetime, steps/burned/calories to int
    df.date = pd.to_datetime(df.date)

    to_int = ['steps', 'total_burned', 'active_burned', 'sedentary']
    df = commas_to_ints(df, to_int)

    df = df.set_index('date')
    df['bmr'] = df.total_burned - df.active_burned

    df['time'] = df.sedentary + df.lightly + df.fairly + df.very

    df['stride'] = df.distance / df.steps * 5280

    df['height'] = df.stride / .415

    df['min_age'] = 27
    df['max_age'] = 32

    df['min_weight'] = ((df.bmr + (5.7 * df.min_age) - (183 * 4.8)) / 13.4) * 2.20462
    df['max_weight'] = ((df.bmr + (5.7 * df.max_age) - (183 * 4.8)) / 13.4) * 2.20462
    return df

def prep_for_prophet(df):
    df = df.drop(columns=['bmr', 'time', 'stride'])
    df = df.rename(columns={'date':'ds'})
    return df

def split(df):
    tss = TimeSeriesSplit(5)
    for train_index, test_index in tss.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
    return train, test

if __name__ == '__main__':
    activity = get_activity()
    activity = prep_activity(activity)