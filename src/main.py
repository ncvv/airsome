''' Main entry point of the project, where the program is launched. '''

import sys

import requests

import io_util as io
import preprocess as pp
#import classifier2 as cl

def main(renew_listings=False):
    ''' Main method. '''
    if renew_listings:
        listings = io.read_csv('../data/original/listings.csv')
        pp.Preprocessor.prepare_listings_data(listings)

    reviews = io.read_csv('../data/original/reviews.csv')
    listings = io.read_csv('../data/processed/listings_processed.csv')
    listings_text = io.read_csv('../data/processed/listings_text_processed.csv')
    preprocessor = pp.Preprocessor(False, requests.Session(), listings, listings_text, reviews)
    preprocessor.process()

    #dataset = io.read_csv('../data/playground/dataset.csv')
    #classifier = cl.Classifier(dataset)
    #for kn in range(1, 10):
        #classifier.classify_knn(dataset, n=kn)
    #classifier.classify_nb()
    #..
    #print(classifier)

if __name__ == '__main__':
    if sys.argv[1:]:
        renew_listings_flag = sys.argv[1]
        main(renew_listings_flag)
    else:
        main()
