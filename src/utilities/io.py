''' Utility methods '''

import os
import csv

import pandas as pd

def read_csv(path):
    ''' Read in a csv as a pandas dataframe. '''
    return pd.read_csv(get_universal_path(path))

# ToDo
#def read_csv_column(path, column_name):
#def read_csv_columns(path, column_names):
#def append_column_to_csv():

def append_to_csv(path, l, header=False, index=False):
    ''' Append content to an existing csv file. '''
    with open(get_universal_path(path), 'a+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(l)

def write_csv(dataframe, path, index=False):
    ''' Write a dataframe to a path as csv. '''
    dataframe.to_csv(get_universal_path(path), sep=',', encoding='utf-8', index=index)

def get_universal_path(file_path):
    ''' Return universal path to file that works on every operating system. '''
    args = file_path.split('/')
    return os.path.join(*args)
