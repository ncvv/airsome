import pandas as pd
#from .tools import helperFunctions

#doc = pd.read_csv("../../data/subset/listings_sub.csv")
doc= pd.read_csv(r"C:\Users\Wifo\Documents\DMProject\DM1-Teamproject\data\subset\listings_sub.csv")
barriers = pd.read_csv(r"C:\Users\Wifo\Dropbox\1 MASTER\1 FS - HWS 2017_8\IE 500 - Data Mining\DM project\Daten\neighbourhoods.csv")

frame = pd.DataFrame(doc)
#print(len(frame.columns))
#get the important cloumn indices
#'host_neighbourhood'
#allColumns = frame.columns
print(frame.columns.values)
one = frame.columns.get_loc('host_neighbourhood')
#'street' 
two = frame.columns.get_loc('street')
#'neighbourhood'
three = frame.columns.get_loc('neighbourhood')
#'neighbourhood_cleansed' 
four = frame.columns.get_loc('neighbourhood_cleansed')
#'neighbourhood_group_cleansed' 
five = frame.columns.get_loc('neighbourhood_group_cleansed')
#'city' 
six = frame.columns.get_loc('city')
#'state'
seven = frame.columns.get_loc('state')
#'zipcode' 
eight = frame.columns.get_loc('zipcode')
'latitude'
nine = frame.columns.get_loc('latitude')
# 'longitude'
ten  = frame.columns.get_loc('longitude')
# 'is_location_exact'
eleven = frame.columns.get_loc('is_location_exact')
#print(frame.columns.values)
'''print(one)
print("\n")
'''

#print(frame.head())
cutFrame = frame[['host_neighbourhood', 'street','neighbourhood','neighbourhood_cleansed','city','state', 'zipcode','latitude','longitude','is_location_exact']]#.unique()

#print(cutFrame)
#print(cutFrame.head())

#List unique values in the df['name'] column
#df.name.unique()
# show me the unique values in each column
'''column_list = cutFrame.columns.values.tolist()
for column_name in column_list:
    print(df."[column_name]".unique())
'''
def uniqueValues(table):
    for col in table:
        print(col)
        print(table[col].unique())
        print("\n")


uniqueValues(cutFrame)

uniqueValues(barriers)
# there is no neighbourhood group so this can be cut from the table neighbourhoods (1.st col)
