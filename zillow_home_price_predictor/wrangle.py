# Functions in this WRANGLE file:

# get_connection('db') : retrieves databases for use, by name

# get_zillow_data(): acquires Zillow Data from the CodeUp db

# prep_zillow(df): removes nulls, drops duplicates, formats float to int,
# removes 0 value columns for BD/BR/SQ FT

# remove_outliers(df): removes outliers with a z_score > 3.5

# map_counties(df): improves readability by mapping county name to FIPS

# encode_zillow(df): encodes variables with d_type object

# wrangle_zillow(): combination of multiple above functions that produces a 
# complete, clean data set

# fit_and_scale(scaler, train, validate, test): scaler function for X datasets

#____________________________________________________________________________________

# Required imports for these files:

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import env
import os
import sklearn.preprocessing
from sklearn.model_selection import train_test_split
#____________________________________________________________________________________

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

#____________________________________________________________________________________

def get_zillow_data(use_cache=True):
    """Retrieves zillow data set either from a local CSV (if it exists),
        or from a SQL query to the CodeUp DB.
        Parameters: SELECT bedroomcnt, bathroomcnt, 
		calculatedfinishedsquarefeet AS sq_ft,
        lotsizesquarefeet AS lot_size,
        roomcnt AS room_count,
        taxvaluedollarcnt AS tax_assessed_price, 
        yearbuilt, taxamount, fips AS county, pred_2017.logerror for all Single Family
        Residential in properties_2017 data set, predictions_2017 data set (inferred and labeled)"""
    filename = "zillow.csv"
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = pd.read_sql("""
        SELECT bedroomcnt, bathroomcnt, 
		calculatedfinishedsquarefeet AS sq_ft,
        lotsizesquarefeet AS lot_size,
        roomcnt AS room_count,
        taxvaluedollarcnt AS tax_assessed_price, 
        yearbuilt, taxamount, fips AS county
        FROM properties_2017
        JOIN propertylandusetype USING (propertylandusetypeid)
        JOIN predictions_2017 AS pred_2017 USING (parcelid)
        WHERE (propertylandusetypeid = 261) 
        OR (propertylandusetypeid = 279);
        """
        , get_connection('zillow'))
        df.to_csv(filename, index=False)
        return df
#__________________________________________________________________________________
# outlier handling to remove quant_cols with >3.5 z-score (std dev)
def remove_outliers(threshold, quant_cols, df):
    z = np.abs((stats.zscore(df[quant_cols])))
    df_without_outliers=  df[(z < threshold).all(axis=1)]
    print(df.shape)
    print(df_without_outliers.shape)
    return df_without_outliers

#__________________________________________________________________________________
def map_counties(df):
    # identified counties for fips codes 
    counties = {6037: 'los_angeles',
                6059: 'orange_county',
                6111: 'ventura'}
    # map counties to fips codes
    df.county = df.county.map(counties)
    return df
# make sure 'fips' is object type 
#__________________________________________________________________________________

def prep_zillow(df):
    """
    Takes in zillow Dataframe from the get_zillow_data function.
    Arguments: drops unnecessary columns, 0 value columns, duplicates,
    and converts select columns from float to int.
    Returns cleaned data.
    """
    # remove empty entries stored as whitespace, convert to nulls
    df = df.replace(r'^\s*$', np.nan, regex=True)
    # drop null rows
    df = df.dropna()
    # drop any duplicate rows
    df = df.drop_duplicates(keep='first')
    # convert column types from float to int
    df = df.astype({'county': object})
    # remove homes with 0 BR/BD or SQ FT from the final df
    df = df[(df.bedroomcnt != 0) & (df.bathroomcnt != 0) & 
    (df.sq_ft >= 69)]
    # remove all rows where any column has z score gtr than 3
    non_quants = ['county']
    quants = df.drop(columns=non_quants).columns
    # outlier handling
    # remove numeric values with > 3.5 std dev
    df = remove_outliers(3.5, quants, df)
    df = map_counties(df)

    return df
#__________________________________________________________________________________
#scaler = sklearn.preprocessing.MinMaxScaler()
#scaler = sklearn.preprocessing.StandardScaler()
#scaler = sklearn.preprocessing.RobustScaler()
#pick the scaler and specify in the parameters


def fit_and_scale(scaler, train, validate, test):
    # only scales float columns
    floats = train.select_dtypes(include='float64').columns
    # fits scaler to training data only, then transforms
    # train, validate & test
    scaler.fit(train[floats])
    scaled_train = pd.DataFrame(data=scaler.transform(train[floats]), columns=floats)
    scaled_validate = pd.DataFrame(data=scaler.transform(validate[floats]), columns=floats)
    scaled_test = pd.DataFrame(data=scaler.transform(test[floats]), columns=floats)
    return scaled_train, scaled_validate, scaled_test

#__________________________________________________________________________________
def encode_zillow(df):
    """
    Takes in Zillow Dataframe.
    Encodes categorical data.    
    Returns encoded_df.
    """
    #Get dummies for non-binary categorical variables:
    dummies_list = df.select_dtypes('object').columns
    dummy_df = pd.get_dummies(df[dummies_list], dummy_na = False, drop_first=True)
    #concatenate the two dataframes
    df = pd.concat([df, dummy_df], axis=1)
    #rename the encoded df
    encoded_df = df.drop(columns=dummies_list)
    #return the encoded df
    return encoded_df
#__________________________________________________________________________________

def wrangle_zillow():
    df = get_zillow_data()
    df = prep_zillow(df)
    df = encode_zillow(df)
    return df

#__________________________________________________________________________________


