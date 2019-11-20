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
                'Floors': 'floors', 'Minutes Sedentary': 'out', 'Minutes Lightly Active': 'fat_burn',
                'Minutes Fairly Active': 'cardio', 'Minutes Very Active': 'peak', 'Activity Calories': 'active_burned'}

    df = df.rename(columns=lazy_names)

    # change datatypes to more appropriate ones
    # date to datetime, steps/burned/calories to int
    df.date = pd.to_datetime(df.date)

    to_int = ['steps', 'total_burned', 'active_burned', 'out']
    df = commas_to_ints(df, to_int)

    df = df.set_index('date')
    df = df.sort_index()

    # Basal Metabolic Rate, amount of calories burned per day at rest
    df['bmr'] = df.total_burned - df.active_burned

    # total time spent with the fitbit running
    df['time'] = df.out + df.fat_burn + df.cardio + df.peak

    # stride length in feet
    df['stride'] = df.distance / df.steps * 5280

    # height in feet
    df['height'] = df.stride / .415

    # assumed age range. minimum age ensures weight doesn't go below
    df['min_age'] = 27
    df['max_age'] = 32

    df['min_weight'] = ((df.bmr + (5.7 * df.min_age) - (183 * 4.8)) / 13.4) * 2.20462
    df['max_weight'] = ((df.bmr + (5.7 * df.max_age) - (183 * 4.8)) / 13.4) * 2.20462
    return df

def prep_for_prophet(df):
    df = df[['date', 'total_burned', 'steps', 'distance', 'floors', 'out', 'fat_burn', 'cardio', 'peak', 'active_burned']]
    df = df.rename(columns={'date':'ds'})
    df.loc[df['active_burned'] < 100, 'active_burned'] = None
    df.loc[df['fat_burn'] < 25, 'fat_burn'] = None
    df.loc[(df.out == 1440) | (df.out < 400), 'out'] = None
    df.loc[df.floors > 30, 'floors'] = None
    df.loc[df.distance < .1, 'distance'] = None
    df.loc[df.steps < 100, 'steps'] = None
    df.loc[df.total_burned < 1000, 'total_burned'] = None
    return df

def split(df):
    tss = TimeSeriesSplit(5)
    for train_index, test_index in tss.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
    return train, test

if __name__ == '__main__':
    activity = get_activity()
    activity = prep_activity(activity)