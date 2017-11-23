''' Main entry point of the project, where the program is launched. '''

import requests

import io_util as io
import preprocess as pp
#import classifier2 as cl

import pandas as pd

def main():
    ''' Main method. '''
    listings = io.read_csv('../data/original/listings.csv')
    pp.prepare_listings_data(listings)

    reviews = io.read_csv('../data/original/reviews.csv')
    listings = io.read_csv('../data/processed/listings_processed.csv')
    listings_text = io.read_csv('../data/processed/listings_text_processed.csv')
    preprocessor = pp.Preprocessor(False, requests.Session(), listings, listings_text, reviews)
    preprocessor.process()

    dataset = io.read_csv('../data/playground/dataset.csv')
    #classifier = cl.Classifier(dataset)
    #classifier.classify_nb()
    #..
    #print(classifier)

if __name__ == '__main__':
    main()
