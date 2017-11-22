import pandas as pd
import io_util as io
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import numpy as np
from sklearn.svm import SVC
from sklearn import preprocessing
from category_encoders.ordinal import OrdinalEncoder
import category_encoders as ce
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV

def svm(dataset):  
    #print(dataset.columns)
    
    cols = ['id', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'price',
       'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people',
       'minimum_nights', 'maximum_nights', 'availability_30',
       'availability_60', 'availability_90', 'availability_365',
       'number_of_reviews', 'review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location',
       'review_scores_value', 'calculated_host_listings_count',
       'reviews_per_month', 'experiences_offered', 'host_name', 'host_since',
       'host_location', 'host_response_time', 'host_is_superhost',
       'host_has_profile_pic', 'host_identity_verified',
       'neighbourhood_cleansed', 'zipcode', 'is_location_exact',
       'property_type', 'room_type', 'bed_type', 'calendar_updated',
       'first_review', 'last_review', 'instant_bookable',
       'cancellation_policy', 'require_guest_profile_picture',
       'require_guest_phone_verification', 'host_response_rate_binned',
       'host_verification_binned', 'perceived_quality']
    cols2 = [  'maximum_nights', 'host_name', 'host_since',
    'host_location', 'host_response_time','first_review', 'last_review']
     #accuracy_per_column(cols2, dataset)

    #attr = dataset[['beds', 'security_deposit', 'guests_included', 'availability_30', 'availability_60', 'availability_90', 'availability_365', 'review_scores_accuracy', 'review_scores_checkin', 'review_scores_cleanliness', 'review_scores_communication', 'review_scores_location', 'review_scores_value', 'host_is_superhost', 'instant_bookable', 'cancellation_policy']]
    #attr = dataset[['beds', 'security_deposit', 'guests_included',  'availability_365', 'review_scores_accuracy', 'review_scores_checkin', 'review_scores_cleanliness',  'review_scores_value', 'host_is_superhost', 'instant_bookable', 'cancellation_policy']]
    #attr = dataset[['beds', 'security_deposit', 'guests_included',   'review_scores_cleanliness',  'review_scores_value' ]]
    attr = dataset[[  'review_scores_cleanliness',  'review_scores_value' ]] #Accuracy SVM:0.825136612021858
    attr = dataset[[  'security_deposit', 'review_scores_cleanliness',  'review_scores_value' ]] #Accuracy SVM:0.825136612021858
    

    target_label = dataset['perceived_quality']
    
    one_way(attr, target_label)
    
    #using_GridSearch(attr, target_label)
    
    '''
    accuracy_rating = cross_val_score(decision_tree,score_data,score_target_binned,cv = 10, scoring ='accuracy')
    print(accuracy_rating.mean())
    '''

def accuracy_per_column(cols, dataset):
    for column in cols:
        print(column)
        attr = dataset[str(column)]
        attr = attr.values.reshape(-1,1) # only needed if there is  one attribute
        target_label = dataset['perceived_quality']
        one_way(attr, target_label)

def one_way(attr, target_label):
    clf = SVC(kernel='linear')#, decision_function_shape='ovr')
    #attr = attr.values.reshape(-1,1)
    data_train, data_test, target_train, target_test =  split_dataset_regular(attr, target_label) #, test_size=0.2, random_state=42, stratify=target_label)
    
    clf.fit(data_train, target_train)
    pred = clf.predict(data_test)
    acc=accuracy_score(target_test, pred)
    print('Accuracy SVM:{}'.format(acc))
    #print('SVM score:{}'.format(clf.score))

def using_GridSearch(attr, target_label):
    clf = SVC()
    parameters = {
        'kernel':['linear', 'rbf'],#'poly',  'sigmoid', 'precomputed'] # POLY läuft heiß bei mir, precomputed gar nicht
        'C': [1.0, 1.5, 0.5]# penalty parameter
        #'degree': [3,4,5,6,7,8] # for poly only
        #'gamma': [],#Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. If gamma is ‘auto’ then 1/n_features will be used instead.
        #'coef0': [],#Independent term in kernexl function. It is only significant in ‘poly’ and ‘sigmoid’
        #'tol':[] ,#Tolerance for stopping criterion
        #'decision_function_shape': ['ovo', 'ovr']
    }

    cv = StratifiedKFold(n_splits=20, shuffle=True, random_state=42)
    grid_search_estimator = GridSearchCV(clf, parameters, scoring='accuracy', cv=cv)
    grid_search_estimator.fit(attr, target_label)
    print("best score is {} with params {}".format(grid_search_estimator.best_score_, grid_search_estimator.best_params_ ))

    results = grid_search_estimator.cv_results_
    for i in range(len(results['params'])):
       print(results['mean_test_score'][i])
       # print("{}, {}".format(results['params'][i], results['mean_test_score'][i]))


def encode_hole_dataset(dataset, save, filename):
    from category_encoders.ordinal import OrdinalEncoder
    from category_encoders.ordinal import OrdinalEncoder
    import pandas as pd
    import io_util as io

    #encoder = ce.OneHotEncoder()
    encoder = OrdinalEncoder()
    data_encoded = encoder.fit_transform(dataset)
    print(data_encoded.head())
    if (save):
        path = '../data/playground/' + filename + '.csv'
        print (path)
        io.write_csv(data_encoded, path )


def init ():
    listings = io.read_csv('../data/playground/dataset.csv')
    encode_hole_dataset(listings, True, 'encoded_listings')

def split_dataset_specific(data, target, test_size, stratify_target):
    if (stratify_target):
        data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=test_size, random_state=42, stratify=target)
    else:
        data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=test_size, random_state=42)
    return data_train, data_test, target_train, target_test

def split_dataset_regular(data, target):
    return split_dataset_specific(data, target, test_size=0.2, stratify_target=True)


#init()

encoded_listings = listings = io.read_csv('../data/playground/encoded_listings.csv')
svm (encoded_listings)
print('Done')
#svm(listings)

