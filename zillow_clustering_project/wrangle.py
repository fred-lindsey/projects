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

#_______________________________________________________________________________________
# handles missing values, drops columns that are 30% empty, drops rows that are 25% empty
# drops duplicate columns as well
def handle_missing_values(df, prop_required_column = .7, prop_required_row=.75):
    threshold = int(round(prop_required_column*len(df.index), 0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns), 0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    df = df.drop_duplicates(keep='first')
    return df

#_______________________________________________________________________________________
# handles missing values, drops columns that are 30% empty, drops rows that are 25% empty
# drops duplicate columns as well
def handle_remaining_nulls(df):
    null_columns = ['lotsizesquarefeet', 'yearbuilt', 'calculatedfinishedsquarefeet','taxvaluedollarcnt']
    for col in null_columns:
        df[col] = df[col].fillna(df[col].mean())
    return df

#__________________________________________________________________________________
# these columns needed to be removed because they added no useful information, and 
# regionidzip caused an issue in data wrangling

def remove_columns(df):
    cols_to_remove = ['propertylandusetypeid', 'id', 'id.1', 'finishedsquarefeet12', 
    'regionidzip', 'rawcensustractandblock', 'assessmentyear', 'censustractandblock',
    'regionidcity', 'taxamount', 'landtaxvaluedollarcnt', 'structuretaxvaluedollarcnt',
    'fullbathcnt', 'calculatedbathnbr', 'parcelid', 'regionidcounty', 'parcelid', 
    'propertycountylandusecode', 'propertylandusedesc']
    df = df.drop(columns=cols_to_remove)
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
def convert_data_types(df):
    # identified columns to change to object types, for later encoding
    non_quant_cols = ['fips', 'latitude', 'longitude']
    for col in non_quant_cols:
        df[col] = df[col].astype('object')
    return df
#__________________________________________________________________________________
# outlier handling to remove quant_cols with >3 z-score (std dev) for float columns 
# other than the target variable. threshold is the level of zscore or standard deviations
# from the mean, which the function will use as a ceiling
# eliminte nulls first

def remove_outliers(df, threshold=3):
     # set quant_cols 
    quant_cols = []
    for col in df.columns:
        if df[col].dtype == 'float64' and col != 'logerror':
            quant_cols.append(col)
    print(quant_cols)
    # remove df rows where z_score > 3.5 for quant_cols
    z = np.abs((stats.zscore(df[quant_cols])))
    print(z)
    df = df[(z < threshold).all(axis=1)]
    print(df.head(20))
    # remove homes with 0 BR/BD or SQ FT from the final df
    df = df[(df.bedroomcnt != 0) & (df.bathroomcnt != 0) & 
    (df.calculatedfinishedsquarefeet >= 69)]
    return df


#__________________________________________________________________________________

#__________________________________________________________________________________

# def q1_logerror(s, k):
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

# def q4_logerror(s, k):
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
def prep_zillow(df):
    """
    Takes in zillow Dataframe from the get_zillow_data function.
    Arguments: 
    threshold, maps county names to FIPS, and removes outliers > 3.5 z score above
    mean.
    Returns cleaned data.
    """
    
    df = handle_missing_values(df)
    df = handle_remaining_nulls(df)
    df = remove_columns(df)
    df = map_counties(df)
    df = convert_data_types(df)
    df = remove_outliers(df, threshold=3)
    return df 
#__________________________________________________________________________________

def wrangle_zillow():
    df = get_zillow_data()
    df = prep_zillow(df)
    return df
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





