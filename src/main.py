''' Main entry point of the code, where the program is launched. '''
import pandas as pd

import utilities.io as io
import preprocessing.preprocess as pp

def inspect_dataset(dataset):
    ''' Dataset inspection method for getting insights on different features, value examples, .. '''
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_colwidth', 120)

    # Access column id
    print(dataset["id"])
    # Join Column names and print them
    print('\n'.join(list(dataset)))
    # Example values of ex. with id 10
    print(dataset.iloc[10])

def main():
    ''' Main method. '''
    reviews = io.read_csv('../data/original/reviews.csv')
    #inspect_dataset(reviews)
    listings = io.read_csv('../data/original/listings.csv')
    #inspect_dataset(listings)

    pp.process_listings(listings)

if __name__ == '__main__':
    main()
