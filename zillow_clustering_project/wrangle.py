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

def get_mall_customers(use_cache=True):
    """Retrieves mall Customer dataset from CodeUp server"""
    filename = "mall_customers.csv"
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = pd.read_sql("""
        SELECT * 
        FROM customers;
        """
        , get_connection('mall_customers'))
        df.to_csv(filename, index=False)
        return df

#____________________________________________________________________________________

def get_zillow_data(use_cache=True):
    """Retrieves predictions_2017, properties_2017, unique_properties, propertylandusetype,
    storytype, and typeconstructiontype tables from the Zillow Dataset"""
    filename = "zillow.csv"
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = pd.read_sql("""
        SELECT * 
        FROM predictions_2017
        LEFT JOIN properties_2017 USING(parcelid)
        LEFT JOIN unique_properties USING(parcelid)
        LEFT JOIN propertylandusetype USING(propertylandusetypeid)
        LEFT JOIN storytype USING(storytypeid)
        LEFT JOIN airconditioningtype USING(airconditioningtypeid)
        LEFT JOIN architecturalstyletype USING(architecturalstyletypeid)
        LEFT JOIN heatingorsystemtype USING(heatingorsystemtypeid)
        LEFT JOIN buildingclasstype USING(buildingclasstypeid)
        LEFT JOIN typeconstructiontype USING(typeconstructiontypeid)
        WHERE transactiondate > 2017-01-01
        AND propertylandusetype.propertylandusedesc = 'Single Family Residential'
        AND latitude IS NOT NULL
        AND longitude IS NOT NULL;
        """
        , get_connection('zillow'))
        df.to_csv(filename, index=False)
        return df
#__________________________________________________________________________________
# outlier handling to remove quant_cols with >3.5 z-score (std dev)

def remove_outliers(threshold, quant_cols, df):
    z = np.abs((stats.zscore(df[quant_cols])))
    df=df[(z < threshold).all(axis=1)]
    # remove homes with 0 BR/BD or SQ FT from the final df
    df = df[(df.bedroomcnt != 0) & (df.bathroomcnt != 0) & 
    (df.calculatedfinishedsquarefeet >= 69)]
    return df

#__________________________________________________________________________________
def map_counties(df):
    # identified counties for fips codes 
    counties = {6037: 'los_angeles',
                6059: 'orange_county',
                6111: 'ventura'}
    # map counties to fips codes
    df.fips = df.fips.map(counties)
    return df
#__________________________________________________________________________________
cols_to_remove = ['heatingorsystemtypeid', 'propertylandusetypeid', 'id', 'id.1',
'buildingqualitytypeid']

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df
#__________________________________________________________________________________
# handles missing values, drops columns that are 50% empty, drops rows that are 25% empty
# drops duplicate columns as well
def handle_missing_values(df, prop_required_column = .5, prop_required_row=0.75):
    threshold = int(round(prop_required_column*len(df.index), 0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns), 0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    df = df.drop_duplicates(keep='first')
    return df
#__________________________________________________________________________________

# def get_upper_outliers(s, k):
#     '''
#     Given a series and a cutoff value, k, returns the upper outliers for the
#     series.

#     The values returned will be either 0 (if the point is not an outlier), or a
#     number that indicates how far away from the upper bound the observation is.
#     '''
#     q1, q3 = s.quantile([.25, .75])
#     iqr = q3 - q1
#     upper_bound = q3 + k * iqr
#     return s.apply(lambda x: max([x - upper_bound, 0]))

#__________________________________________________________________________________

# def get_lower_outliers(s, k):
#     '''
#     Given a series and a cutoff value, k, returns the lower outliers for the
#     series.

#     The values returned will be either 0 (if the point is not an outlier), or a
#     number that indicates how far away from the upper bound the observation is.
#     '''
#     q1, q3 = s.quantile([.25, .75])
#     iqr = q3 - q1
#     lower_bound = q1 - (k * iqr)
#     return s.apply(lambda x: min([x - lower_bound, 0]))

#__________________________________________________________________________________
# def add_outlier_columns(df, k):
#     '''
#     Add a column with the suffix _outliers for all the numeric columns
#     in the given dataframe.
#     '''
#     # outlier_cols = {col + '_outliers': get_upper_outliers(df[col], k)
#     #                 for col in df.select_dtypes('number')}
#     # return df.assign(**outlier_cols)

#     for col in df.select_dtypes('number'):
#         df_outliers = df[col + '_outliers'] = get_upper_outliers(df[col], k)

#     return df_outliers

#__________________________________________________________________________________
def data_prep(df):
    """
    Takes in zillow Dataframe from the get_zillow_data function.
    Arguments: drops unnecessary columns, removes null columns and rows above
    threshold, maps county names to FIPS, and removes outliers > 3.5 z score above
    mean.
    Returns cleaned data.
    """
    
    df = handle_missing_values(df)
    df = remove_columns(df, cols_to_remove)
    df = map_counties(df)
    #df_outliers = add_outlier_columns(df, k=1.5)
    return df #df_outliers


#________________________________________________________
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
    Encodes object type columns.    
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
    df = data_prep(df)
    #df = get_upper_outliers(df, k=1.5)
    return df

#__________________________________________________________________________________

# pred_2017.parcelid AS ID, bedroomcnt, bathroomcnt,
# 		calculatedfinishedsquarefeet AS sq_ft,
#         lotsizesquarefeet AS lot_size,
#         taxvaluedollarcnt AS home_price, 
#         yearbuilt, taxamount, fips AS county, latitude, longitude,
#         pred_2017.logerror AS log_error

#__________________________________________________________________________________
# Original prep zillow function

# def prep_zillow(df):
#     """
#     Takes in zillow Dataframe from the get_zillow_data function.
#     Arguments: drops unnecessary columns, 0 value columns, duplicates,
#     and converts select columns from float to int.
#     Returns cleaned data.
#     """
#     # remove empty entries stored as whitespace, convert to nulls
#     print('before replace whitespace')
#     df = df.replace(r'^\s*$', np.nan, regex=True)
#     print('after replace whitespace')
#     # drop columns with more than 30% null values
#     print('before drop 30% null rows')
#     df = df.dropna(axis=1, thresh=(3*(len(df)/10)))
#     print('before drop 30% null rows')
#     # drop any duplicate rows
#     df = df.drop_duplicates(keep='first')
#     print('before non-quants')
#     # convert column types from float to int
#     non_quants = ['fips', 'parcelid', 'id', 'latitude', 'longitude', 
#     'regionidcity', 'propertylandusetypeid', 'propertyzoningdesc', 'transactiondate',
#      'propertylandusedesc']
#     df[non_quants] = df[non_quants].astype('object')
#     print('after quants')
#     # remove homes with 0 BR/BD or SQ FT from the final df
#     df = df[(df.bedroomcnt != 0) & (df.bathroomcnt != 0) & 
#     (df.calculatedfinishedsquarefeet >= 69)]
#     # remove all rows where any column has z score gtr than 3
#     quants = df.drop(columns=non_quants).columns
#     #quants = df.astype()
#     # outlier handling
#     # remove numeric values with > 3.5 std dev
#     df = remove_outliers(3.5, quants, df)
#     df = map_counties(df)

#     return df
#__________________________
