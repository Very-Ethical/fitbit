import pandas as pd
import os
import csv

def make_activity_csv(dir_name='fitbit'):
    writefile = 'activity.csv'
    write = csv.writer(open(writefile, 'w+'))
    for filename in os.listdir(dir_name):
        with open('fitbit/' + filename) as f:
            reader = csv.reader(f)
            row = ''
            while row != ['Activities']:
                row = next(reader)
            row = next(reader)
            if os.stat(writefile).st_size == 0:
                write.writerow(row)
                write = csv.writer(open(writefile, 'a'))
            row = next(reader)
            while row != []:
                write.writerow(row)
                row = next(reader)


def get_activity():
    activity = pd.read_csv('activity.csv')
    return activity

if __name__ == '__main__':
    make_activity_csv()