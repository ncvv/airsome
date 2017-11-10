''' Main entry point of the code, where the program is launched. '''
import pandas as pd
import utilities.io as io

import subprocess

def inspect_dataset(dataset):
    ''' Dataset inspection method for getting insights on different features, value examples, .. '''
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_colwidth', 50)

    # Access column id
    #print(dataset["id"])
    # Join Column names and print them
    #print('\n'.join(list(dataset)))
    # Example values
    print(dataset.iloc[7])

def main():
    ''' Main method. '''
    #print('Listings Subset: ' + '\n')
    listings_subset = io.read_csv('../data/subset/listings_sub.csv')
    listings = io.read_csv('../data/original/listings.csv')
    #inspect_dataset(listings_subset)

    #print(('\n' * 2) + 'Reviews Subset: ' + '\n')
    reviews_subset = io.read_csv('../data/subset/reviews_sub.csv')
    reviews = io.read_csv('../data/original/reviews.csv')
    #inspect_dataset(reviews_subset)

    drop_list = ['listing_url', 'scrape_id', 'last_scraped', 'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url', 'host_thumbnail_url', 'host_picture_url']
    drop_list.extend(['name', 'summary', 'space', 'description', 'transit', 'house_rules', 'amenities', 'neighborhood_overview', 'notes', 'access', 'interaction', 'host_about'])
    listings_subset.drop(drop_list, axis=1, inplace=True)
    io.write_csv(listings, '../data/processed/listings_sub_processed.csv')

if __name__ == '__main__':
    main()
