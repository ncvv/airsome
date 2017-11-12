''' Utility methods '''

import os
import csv

import pandas as pd

#def remove_column_df(dataframe, col_name):
#    ''' Remove a column from a dataframe. '''
#    dataframe.drop(col_name, axis=1)

#def remove_line_df(dataframe, col_name, value):
#    ''' Remove a line from a dataframe in the given column with a specific value.
#        If more than one line apply, remove all of them (e.g. price > 800) '''
#    print()

#def append_column_df(dataframe, col_name, dct):
#    ''' Append a column to a dataframe. '''
#    print()

#def append_line_df(dataframe, lst):
            
def read_csv(path):
    ''' Read in a .csv file and return it as a pandas dataframe. '''
    return pd.read_csv(get_universal_path(path))

def append_line_csv(path, lst, header=False, index=False):
    ''' Append a list of one or more lines to an existing csv file. '''
    with open(get_universal_path(path), 'a+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        if not isinstance(lst[0], list):
            writer.writerow(lst)
        else:
            for line in lst:
                writer.writerow(line)

def write_csv(dataframe, path, index=False):
    ''' Write a pandas dataframe to the given path as .csv file. '''
    dataframe.to_csv(get_universal_path(path), sep=',', encoding='utf-8', index=index)

def get_universal_path(file_path):
    ''' Return universal path to file that works on every operating system. '''
    args = file_path.split('/')
    return os.path.join(*args)

#def sort_df_by_id(dataframe, ascending=True):

