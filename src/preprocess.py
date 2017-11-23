
''' Preprocessing module containing all methods of data cleansing and
    tokenizing, stemming as well as stopword removal. '''

import re
import ast

from langdetect import detect

import io_util as io

import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

class Preprocessor(object):
    ''' Preprocesses data with different methods. '''

    def __init__(self, crawl, session, listings_data, listings_text_data, reviews_data):
        self.crawl = crawl
        self.ses = session
        self.listings = listings_data
        self.listings_text = listings_text_data
        self.reviews = reviews_data
        self.removal_ids = []
        self.review_removal_ids = []

    # See commit 8f9d8e1f for implementation of writing results to a .csv.
    def check_onair(self):
        ''' Checks how many of the listing ids are still online@Airbnb. '''
        air_url = 'https://www.airbnb.de/rooms/'
        ids = self.listings['id']
        num_apts = len(ids)
        for i in ids.tolist():
            url = air_url + str(i)
            try:
                # content-length only in header if listing is not available anymore (not on Air)
                content_length = self.ses.get(url).headers.__getitem__('content-length')
                print(str(i) + ' is not on Air anymore; content-length: ' + str(content_length))
                num_apts -= 1
            except KeyError:
                print(str(i) + ' is still on Air.')
        print('{0:.2f}% of Apartments are still on Air.'.format(float(num_apts / len(ids)) * 100))
    
    def inspect_dataset(self):
        ''' Dataset inspection method for getting insights on different features, value examples, .. '''
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_colwidth', 120)

        # Access column id
        print(self.listings["id"])
        # Join Column names and print them
        print('\n'.join(list(self.listings)))
        # Example values of ex. with id 10
        print(self.listings.iloc[10])

    def bin_host_rate(self, df):
        ''' Bin the values of host_response_rate. '''
        bins = [0, 50, 85, 99, 100]
        grp_names = ['Bad', 'Medium', 'Good', 'Very Good']
        df['host_response_rate'] = df['host_response_rate'].apply(lambda x: int(x.replace('%', '')))
        df['host_response_rate_binned'] = pd.cut(df['host_response_rate'], bins, labels=grp_names)
        df.loc[df['host_response_rate'] == 0, 'host_response_rate_binned'] = 'Bad'
        df.drop('host_response_rate', axis=1, inplace=True)
    
    def bin_host_location(self, df):
        ''' Bin the values of host_location. '''
        df['host_location'] = df['host_location'].apply(lambda x: 'inlondon' if 'lon' in str(x).lower() else 'notinlondon')

    def bin_host_verification(self, df):
        ''' Bin the host verification. '''
        # Host Verifications: {'jumio', 'sent_id', 'sesame', 'linkedin', 'kba', 'manual_offline', 'facebook', 'offline_government_id', 'photographer', 'amex', 'email', 'phone', 'sesame_offline', 'weibo', 'manual_online', 'government_id', 'google', 'reviews', 'selfie'}
        # Distribution {4: 10142, 3: 5213, 6: 2313, 5: 5078, 2: 339, 7: 475, 8: 78, 1: 10, 9: 5, 10: 1}
        # Max: 19, Most verification methods for one host: 10, Most ofen: 4
        bins = [0, 3, 4, 10]
        grp_names = ['LowerThan4', 'Equals4', 'MoreThan4']
        df['host_verifications'] = df['host_verifications'].apply(lambda x: int(len(ast.literal_eval(x))))
        df['host_verification_binned'] = pd.cut(df['host_verifications'], bins, labels=grp_names)
        df.drop('host_verifications', axis=1, inplace=True)

    def delete_dollar(self, df):
        ''' Delete $ from columns with a price and cast it to int. '''
        df[['price', 'security_deposit', 'cleaning_fee', 'extra_people']] = df[['price', 'security_deposit', 'cleaning_fee', 'extra_people']].applymap(lambda x: float(str(x).replace('$', '').split('.')[0].replace(',', '.')))

    def create_label(self, df, num_labels):
        ''' Create the label from review_scores_rating. '''
        label_name = 'perceived_quality'
        if num_labels == 2:
            bins = [0, 93, 100]
            grp_names = ['Bad', 'Good']
        elif num_labels == 5:
            bins = [0, 65, 75, 90, 95, 100]
            grp_names = ['Catastrophic', 'Bad', 'Medium', 'Good', 'Very Good']
        else:
            raise ValueError("#Labels must be in [2, 5]")
        df[label_name] = pd.cut(df['review_scores_rating'], bins, labels=grp_names)
        df.drop('review_scores_rating', axis=1, inplace=True)

    def normalize(self, df, column_list):
        ''' Min/Max normalization of columns. '''
        pd.options.display.float_format = '{:,.8f}'.format
        for feature in column_list:
            max_value = df[feature].max()
            min_value = df[feature].min()
            df[feature] = (df[feature] - min_value) / (max_value - min_value)

    def clean_zipcodes(self, df):
        ''' Clean the zipcodes and write to clean_zipcodes.csv '''
        dct = io.get_column_as_dict_df(df, 'zipcode')
        for id_value, zipcode in dct.items():
            if zipcode is not None and zipcode is not np.nan:
                zipcode = str(zipcode).upper()
                split = re.split(r'\s+', zipcode.strip().replace('\"', ''))
                if split[0].isalnum():
                    dct[id_value] = split[0]
                else:
                    dct[id_value] = np.nan
            else:
                dct[id_value] = np.nan
        return dct

    def parse_amenities(self, df):
        ''' Parse every value of amenities to binary feature vector. '''
        dct_am = io.get_column_as_dict_df(df, 'amenities')
        dct_am.update({k: v.replace("\"", '').replace("translation missing: en.hosting_amenity_", '').replace('{', '').replace('}', '').split(',') for k,v in dct_am.items()})
        amenities_count = {}
        for key, amenities in dct_am.items():
            for amenity in amenities:
                if amenity not in ['49', '50', '', 'Washer / Dryer']:
                    amenities_count[amenity] = amenities_count.get(amenity, 0) + 1
        for amenity_key in amenities_count.keys():
            column = {}
            for key, am_of_listing in dct_am.items():
                if amenity_key in am_of_listing:
                    column[key] = 1
                else:
                    column[key] = 0
            col_name = 'Amenity_' + str(amenity_key).replace(' ','')
            io.append_dict_as_column_df(df, col_name, column)

    def process_text(self, df, col_name, top_x = 100):
        ''' Tokenize, stem, remove stopwords and apply TFIDF to given text column. '''
        print('h')
    
    # Unused
    def check_language(self, df):
        ''' Remove English reviews. '''
        dct = io.get_column_as_dict_df(df, 'comments')
        for i, comment in dct.items():
            try:
                if detect(comment) != 'en':
                    self.review_removal_ids.append(i)
            except:
                self.review_removal_ids.append(i)

    def process(self):
        ''' Main preprocessing method where all parts are tied together. '''
        # Crawl Airbnb.com page and check if listings are still available
        if self.crawl:
            self.check_onair()

        # Remove lines from pandas dataframe with empty values in these columns
        self.listings.dropna(subset=['host_response_rate', 'review_scores_rating', 'security_deposit', 'cleaning_fee', 'bathrooms', 'bedrooms', 'beds'], inplace=True)

        # Remove all rows where number of reviews < 3
        self.listings = self.listings[self.listings.number_of_reviews > 2]
        
        # Remove all rows where maximum/minimum nights are > X + 1 days
        self.listings = self.listings[self.listings.maximum_nights < 9999]
        self.listings = self.listings[self.listings.minimum_nights < 999]
        
        # Parse zipcodes
        self.listings.loc[:, ['zipcode']].fillna(np.nan, inplace=True)
        dct = self.clean_zipcodes(self.listings)
        self.listings = io.append_dict_as_column_df(self.listings, 'zipcode', dct)
        self.listings.dropna(subset=['zipcode'], inplace=True)

        # Bin host rate, host location and host verification
        self.bin_host_rate(self.listings)
        self.bin_host_location(self.listings)
        self.bin_host_verification(self.listings)

        # Parse $values
        self.delete_dollar(self.listings)

        # Create and append label
        self.create_label(self.listings, 2)

        self.listings_text.dropna(subset=['transit', 'house_rules', 'description', 'neighborhood_overview'], inplace=True)
        self.parse_amenities(self.listings_text)
        self.listings_text.drop('amenities', axis=1, inplace=True)

        #self.process_text(self.listings_text, 'transit')

        # Normalize columns with numeric values
        self.normalize(self.listings, column_list = ['accommodates', 'bathrooms', 'bedrooms', 'beds', 'price', 'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people', 'minimum_nights', 'maximum_nights', 'availability_30', 'availability_60', 'availability_90', 'availability_365', 'number_of_reviews', 'calculated_host_listings_count'])

        # After all processing steps are done in listings and listings_text_processed, merge them on key = 'id'
        self.listings = io.merge_df(self.listings, self.listings_text, 'id')

        ''' Usage of Reviews in our classification is discouraged by Prof. '''
        # Remove reviews that are not english
        #self.reviews = self.reviews.dropna(axis=0, how='any')
        #self.check_language(self.reviews)

        # Remove all of the ids in reviews_removal_ids from the listings
        #self.reviews = io.remove_lines_by_id_df(self.reviews, self.review_removal_ids)

        # After all processing setps are done in reviews.csv and processed text is grouped by id, merge it with listings
        # Maybe we have to overthink this (for example: do we have columns with the same name in the processed listings_text and reviews?
        #                                  Avoid this by appending _lt or _rev at the new columns' names)
        #self.listings = io.merge_df(self.listings, self.reviews, 'id')
        ''' Usage of Reviews in our classification is discouraged by Prof. '''

        # After all processing steps are done, write the listings file to the playground (this will be changed to ../data/final/_.csv)
        print('#Examples in the end: ' + str(len(self.listings))) # Printing the number of resulting examples for testing purposes and validation
        #self.listings.drop('id', axis=1, inplace=True)
        io.write_csv(self.listings, '../data/playground/dataset.csv')

def prepare_listings_data(listings):
    ''' Process listings and split into two files,
        one file with id and unprocessed text features and (listings_text_processed)
        one file with id and non-textual features (listings_processed). '''
    listings_text = listings[['id', 'transit', 'house_rules', 'amenities', 'description', 'neighborhood_overview']]

    drop_list = ['listing_url', 'scrape_id', 'last_scraped', 'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url', 'host_thumbnail_url', 'host_picture_url']
    drop_list.extend(['review_scores_cleanliness', 'review_scores_accuracy', 'review_scores_checkin', 'review_scores_communication', 'review_scores_location', 'review_scores_value'])
    drop_list.extend(['host_acceptance_rate', 'neighbourhood', 'neighbourhood_group_cleansed', 'license', 'jurisdiction_names', 'has_availability', 'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'street', 'city', 'state', 'market', 'smart_location', 'country', 'monthly_price', 'weekly_price', 'calendar_last_scraped', 'requires_license'])
    drop_list.extend(['name', 'summary', 'space', 'host_about', 'access', 'interaction', 'notes']) # text that is dropped
    drop_list.extend(['transit', 'house_rules', 'amenities', 'description', 'neighborhood_overview']) # text that is preserved with listing id in listings_text_processed.csv
    drop_list.extend(['square_feet', 'country_code', 'host_id', 'longitude', 'latitude']) # drop other columns that are not valuable for classification but are left in til the end for understanding the dataset and validating it
    drop_list.extend(['host_name', 'host_since', 'calendar_updated', 'host_has_profile_pic', 'host_identity_verified', 'is_location_exact']) # 'Remove anything that is not related to the apartment'
    listings.drop(drop_list, axis=1, inplace=True)

    io.write_csv(listings, '../data/processed/listings_processed.csv')
    io.write_csv(listings_text, '../data/processed/listings_text_processed.csv')