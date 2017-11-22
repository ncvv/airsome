import pandas as pd
import io_util as io

from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from category_encoders.ordinal import OrdinalEncoder
from sklearn.metrics import accuracy_score

dataset = io.read_csv('../data/playground/dataset.csv')

encoder = OrdinalEncoder()
        
dataset_encoded = encoder.fit_transform(dataset[['experiences_offered', 'host_name', 'host_since', 'host_location', 'host_response_time', 'host_is_superhost',
                                                        'host_has_profile_pic', 'host_identity_verified', 'neighbourhood_cleansed', 'review_scores_value', 'instant_bookable',
                                                        'cancellation_policy', 'require_guest_profile_picture', 'require_guest_phone_verification', 'calculated_host_listings_count',
                                                        'reviews_per_month', 'host_response_rate_binned', 'host_verification_binned', 'perceived_quality']])

#knn_estimator = KNeighborsClassifier(7)
#knn_estimator.fit(dataset_encoded, dataset['perceived_quality'])
 
data_train, data_test, target_train, target_test = train_test_split(dataset_encoded, dataset['perceived_quality'], test_size=0.2, random_state=42, stratify=dataset['perceived_quality'])


knn_estimator = KNeighborsClassifier(7)
knn_estimator.fit(data_train, target_train)
prediction = knn_estimator.predict(data_test)

accuracy = knn_estimator.score(target_test, prediction)
print(accuracy)