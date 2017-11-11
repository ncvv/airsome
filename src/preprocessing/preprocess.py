
''' Preprocessing module containing all methods of data cleansing and
    tokenizing,stemming as well as stopword removal. '''

import csv

import sys
sys.path.append('../')

import pandas as pd

import tokenize as tkn
import utilities.io as io

class Preprocessor(object):
    ''' Preprocesses data with different methods. '''

    def __init__(self, session, listings_data, listings_text_data, reviews_data):
        self.s = session
        self.listings = listings_data
        self.listings_text = listings_text_data
        self.reviews = reviews_data
  
    def check_onair(self):
        air_url = 'https://www.airbnb.de/rooms/'
        ids = self.listings['id']
        num_apts = len(ids)
        total = 0
        for i in ids.tolist():
            url = air_url + str(i)
            total += 1
            try:
                # content-length only in header if listing is not available anymore. not on air
                r = self.s.get(url).headers.__getitem__('content-length')
                num_apts -= 1
                sys.stdout.write('\rTotal: ' + str(total))
                io.append_to_csv('../data/playground/results_on_air.csv', [i, 0])
            except KeyError:
                #pass
                sys.stdout.write('\rTotal: ' + str(total))
                io.append_to_csv('../data/playground/results_on_air.csv', [i, 1])
        print('{0:.2f}% of Apartments are still on Air.'.format(float(num_apts / len(ids)) * 100))

    def process(self):
        ''' Main preprocessing method where all parts are tied together. '''
        # Order of this process, see process_order.txt
        self.check_onair()

def process_listings(listings):
    ''' Process listings and split into two files,
        one file with id and unprocessed text features and (listings_text_processed)
        one file with id and non-textual features (listings_processed). '''

    listings_text = listings[['id', 'transit', 'house_rules', 'amenities', 'description', 'neighborhood_overview']]

    drop_list = ['listing_url', 'scrape_id', 'last_scraped', 'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url', 'host_thumbnail_url', 'host_picture_url']
    drop_list.extend(['host_acceptance_rate', 'neighbourhood', 'neighbourhood_group_cleansed', 'license', 'jurisdiction_names', 'has_availability', 'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'street', 'city', 'state', 'market', 'smart_location', 'country', 'monthly_price', 'weekly_price', 'calendar_last_scraped', 'requires_license'])
    drop_list.extend(['name', 'summary', 'space', 'host_about', 'access', 'interaction', 'notes']) # text that is dropped
    drop_list.extend(['transit', 'house_rules', 'amenities', 'description', 'neighborhood_overview']) # text that is preserved with listing id in listings_text_processed.csv
    listings.drop(drop_list, axis=1, inplace=True)

    io.write_csv(listings, '../data/processed/listings_processed.csv')
    io.write_csv(listings_text, '../data/processed/listings_text_processed.csv')
