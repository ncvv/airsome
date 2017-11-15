import pandas as pd
import re
import sys
sys.path.append("../")
import pandas as pd
import src.utilities.io as io

whole_file = io.read_csv("../data/processed/listings_processed.csv")
#print(whole_file.shape)
zipcode_col = whole_file[['id','zipcode']]
zipcode_col= pd.DataFrame(zipcode_col)
#print(zipcode_col.shape)

# only for testing 
io.write_csv(zipcode_col, '../data/playground/onlyzipcodes.csv')

#make them all upper case
#upperase = zipcode_col['zipcode'].applymap(lambda x: str(x).upper())
zipcode_col['zipcode'] = zipcode_col['zipcode'].map(lambda x: str(x).upper())
uppercase=zipcode_col
#print(uppercase.shape)
#make it a list with strings
list_str= uppercase['zipcode'].astype(str).values.tolist()

#manipulate data
# for each value in column - get value - trim  - remove " - split - just take first entry as new cleaned
list_clean=[]
for idx in list_str:
    val =idx
    splits = re.split("\s+", val.strip().replace("\"", ""))
    if (splits[0]==""):
         clean_zip_val="NAN"
    elif (splits[0].isalnum()):
        #print("yes")
        clean_zip_val=splits[0]
    else:
        #print("no")
        clean_zip_val="NAN"
    list_clean.append(clean_zip_val)


zipcode_col[:1]
clean_zipcodes =zipcode_col.assign(zipcode=list_clean)


io.write_csv(clean_zipcodes, '../data/playground/clean_zipcodes.csv')
if (zipcode_col.shape[0] == uppercase.shape[0] and uppercase.shape[0]==whole_file.shape[0]):
    print("All rows still intact! :)")


#TODO Problem
'''

15109570,"SE1 5QL

SE1 5QL"
9473453,SE22 0HF
'''
