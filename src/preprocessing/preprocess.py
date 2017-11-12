
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

    # See commit 8f9d8e1f for implementation of csv.
    def check_onair(self):
        ''' Checks how many of the listing ids are still online@Airbnb. '''
        air_url = 'https://www.airbnb.de/rooms/'
        ids = self.listings['id']
        num_apts = len(ids)
        
        res_path = '../data/playground/results_on_air.csv'
        results = io.read_csv(res_path)['id'].tolist()
        total = len(results)

        # Write results to csv file, because 50k listings take a long time.
        # With results written to a file, we can split the process in several runs.
        with open(io.get_universal_path(res_path), 'a+', newline='') as f:
            writer = csv.writer(f, delimiter=',')

            for i in ids.tolist():

                if i in results:
                    print('Bereits vorhanden:' + str(i))
                    continue

                url = air_url + str(i)
                total += 1
                try:
                    # content-length only in header if listing is not available anymore (not on Air)
                    r = self.s.get(url).headers.__getitem__('content-length')
                    num_apts -= 1

                    writer.writerow([i, 0])
                    sys.stdout.write('\rTotal: ' + str(total))
                
                except KeyError:

                    writer.writerow([i, 1])
                    sys.stdout.write('\rTotal: ' + str(total))

            #print('{0:.2f}% of Apartments are still on Air.'.format(float(num_apts / len(ids)) * 100))

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
