# Function dictionary: 
#   - functions contained in this wrangle.py file include:








#_______________________________________________________________________________________________________________________________________________________
#Basic imports needed for these functions to run:

import pandas as pd
import numpy as np
import requests
import os

#_______________________________________________________________________________________________________________________________________________________



# 1. Acquire Grand Canyon NP
# download the GC visitors data from the NPS at the following URL:
# grand_canyon_url = 'https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=GRCA'

def get_gc_visitors(use_cache=True):
        filename = "gc_visitors.csv"
        if os.path.isfile(filename) and use_cache:
            # header=2 will drop the first two lines of the CSV
            return pd.read_csv(filename, header=2)
        else:
            print(""" Download the Grand Canyon visitors dataset at the following URL:
            https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=GRCA
            """)

# 2. Acquire Great Smoky Mountains NP
# download the GSM visitors data from the NPS at the following URL:
# great_smokey_mtns_url = 'https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=GRSM'

def get_gsm_visitors(use_cache=True):
        filename = "gsm_visitors.csv"
        if os.path.isfile(filename) and use_cache:
            # header=2 will drop the first two lines of the CSV
            return pd.read_csv(filename, header=2)
        else:
            print(""" Download the Grand Canyon visitors dataset at the following URL:
            https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=GRSM
            """)

# 3. Acquire Zion NP
# download the Zion visitors data from the NPS at the following URL:
# great_smokey_mtns_url = 'https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=ZION'

def get_zion_visitors(use_cache=True):
        filename = "zion_visitors.csv"
        if os.path.isfile(filename) and use_cache:
            # header=2 will drop the first two lines of the CSV
            return pd.read_csv(filename, header=2)
        else:
            print(""" Download the Grand Canyon visitors dataset at the following URL:
            https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=ZION
            """)

# 4. Acquire Yellowstone NP
# download the Zion visitors data from the NPS at the following URL:
# great_smokey_mtns_url = 'https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=YELL'

def get_yellowstone_visitors(use_cache=True):
        filename = "yellowstone_visitors.csv"
        if os.path.isfile(filename) and use_cache:
            # header=2 will drop the first two lines of the CSV
            return pd.read_csv(filename, header=2)
        else:
            print(""" Download the Grand Canyon visitors dataset at the following URL:
            https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=YELL
            """)

# 5. Acquire Rocky Mountain NP
# download the Zion visitors data from the NPS at the following URL:
# great_smokey_mtns_url = 'https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=ROMO'

def get_rocky_mtn_visitors(use_cache=True):
        filename = "rocky_mtn_visitors.csv"
        if os.path.isfile(filename) and use_cache:
            # header=2 will drop the first two lines of the CSV
            return pd.read_csv(filename, header=2)
        else:
            print(""" Download the Grand Canyon visitors dataset at the following URL:
            https://irma.nps.gov/STATS/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=ROMO
            """)

# 6. Prepare Yellowstone
def prepare_yellowstone(use_cache=True):
    """ This function takes in the dataframe from the get_yellowstone_visitors function, drops the totals column (marked as Textbox5)
    and returns a single column with visitor numbers indexed by month."""
    #use local cache from CSV if available
    filename = 'cleaned_yellowstone_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = get_yellowstone_visitors()
        # set 'Year' as the index, so that I can stack the dataframe, ie reduce the dimensions so that I can merge the dataframes
        df = df.set_index('Year')
        # drop 'Textbox5' column. This is a yearly total column for the dataset
        df = df.drop(columns=['Textbox5'])
        # now I'm going to stack, meaning move the columns headers under the index, to reduce the dimensionality of the dataframe
        df = df.stack(level=0)
        # stacking produces a series when I'm done, and it will need to be converted back into a DF
        df = df.to_frame()
        # now add a title to the DF's only column
        df.columns = ['yellowstone']
        # reset the index to seperate the current multi-index into distinct year and month columns
        df = df.reset_index(drop=False)
        # create a composite date column
        df['date'] = df.Year.astype(str) + "-" + df.level_1
        # convert the date column to datetime object
        df.date = pd.to_datetime(df.date)
        # set the date as the index and sort index
        df = df.set_index('date').sort_index()
        # drop Year and level_1 columns that are no longer needed
        df = df.drop(columns=['Year', 'level_1'])
        df.to_csv(filename, index=True)
        return df

# 7. Prepare Zion
def prepare_zion(use_cache=True):
    """ This function takes in the dataframe from the get_zion_visitors function, drops the totals column (marked as Textbox5)
    and returns a single column with visitor numbers indexed by month."""
    #use local cache from CSV if available
    filename = 'cleaned_zion_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = get_zion_visitors()
        # set 'Year' as the index, so that I can stack the dataframe, ie reduce the dimensions so that I can merge the dataframes
        df = df.set_index('Year')
        # drop 'Textbox5' column. This is a yearly total column for the dataset
        df = df.drop(columns=['Textbox5'])
        # now I'm going to stack, meaning move the columns headers under the index, to reduce the dimensionality of the dataframe
        df = df.stack(level=0)
        # stacking produces a series when I'm done, and it will need to be converted back into a DF
        df = df.to_frame()
        # now add a title to the DF's only column
        df.columns = ['zion']
        # reset the index to seperate the current multi-index into distinct year and month columns
        df = df.reset_index(drop=False)
        # create a composite date column
        df['date'] = df.Year.astype(str) + "-" + df.level_1
        # convert the date column to datetime object
        df.date = pd.to_datetime(df.date)
        # set the date as the index and sort index
        df = df.set_index('date').sort_index()
        # drop Year and level_1 columns that are no longer needed
        df = df.drop(columns=['Year', 'level_1'])
        df.to_csv(filename, index=True)
        return df

# 8. Prepare Grand Canyon
def prepare_grand_canyon(use_cache=True):
    """ This function takes in the dataframe from the get_gc_visitors function, drops the totals column (marked as Textbox5)
    and returns a single column with visitor numbers indexed by month."""
    #use local cache from CSV if available
    filename = 'cleaned_grand_canyon_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = get_gc_visitors()
        # set 'Year' as the index, so that I can stack the dataframe, ie reduce the dimensions so that I can merge the dataframes
        df = df.set_index('Year')
        # drop 'Textbox5' column. This is a yearly total column for the dataset
        df = df.drop(columns=['Textbox5'])
        # now I'm going to stack, meaning move the columns headers under the index, to reduce the dimensionality of the dataframe
        df = df.stack(level=0)
        # stacking produces a series when I'm done, and it will need to be converted back into a DF
        df = df.to_frame()
        # now add a title to the DF's only column
        df.columns = ['grand_canyon']
        # reset the index to seperate the current multi-index into distinct year and month columns
        df = df.reset_index(drop=False)
        # create a composite date column
        df['date'] = df.Year.astype(str) + "-" + df.level_1
        # convert the date column to datetime object
        df.date = pd.to_datetime(df.date)
        # set the date as the index and sort index
        df = df.set_index('date').sort_index()
        # drop Year and level_1 columns that are no longer needed
        df = df.drop(columns=['Year', 'level_1'])
        df.to_csv(filename, index=True)
        return df 

# 9. Prepare Rocky MTN
def prepare_rocky_mtn(use_cache=True):
    """ This function takes in the dataframe from the get_rocky_mtn_visitors function, drops the totals column (marked as Textbox5)
    and returns a single column with visitor numbers indexed by month."""
    #use local cache from CSV if available
    filename = 'cleaned_rocky_mtn_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = get_rocky_mtn_visitors()
        # set 'Year' as the index, so that I can stack the dataframe, ie reduce the dimensions so that I can merge the dataframes
        df = df.set_index('Year')
        # drop 'Textbox5' column. This is a yearly total column for the dataset
        df = df.drop(columns=['Textbox5'])
        # now I'm going to stack, meaning move the columns headers under the index, to reduce the dimensionality of the dataframe
        df = df.stack(level=0)
        # stacking produces a series when I'm done, and it will need to be converted back into a DF
        df = df.to_frame()
        # now add a title to the DF's only column
        df.columns = ['rocky_mtn']
        # reset the index to seperate the current multi-index into distinct year and month columns
        df = df.reset_index(drop=False)
        # create a composite date column
        df['date'] = df.Year.astype(str) + "-" + df.level_1
        # convert the date column to datetime object
        df.date = pd.to_datetime(df.date)
        # set the date as the index and sort index
        df = df.set_index('date').sort_index()
        # drop Year and level_1 columns that are no longer needed
        df = df.drop(columns=['Year', 'level_1'])
        df.to_csv(filename, index=True)
        return df 

# 10. Prepare Great Smoky MTNs
def prepare_great_smoky_mtns(use_cache=True):
    """ This function takes in the dataframe from the get_gsm_visitors function, drops the totals column (marked as Textbox5)
    and returns a single column with visitor numbers indexed by month."""
    #use local cache from CSV if available
    filename = 'cleaned_gsm_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        df = get_gsm_visitors()
        # set 'Year' as the index, so that I can stack the dataframe, ie reduce the dimensions so that I can merge the dataframes
        df = df.set_index('Year')
        # drop 'Textbox5' column. This is a yearly total column for the dataset
        df = df.drop(columns=['Textbox5'])
        # now I'm going to stack, meaning move the columns headers under the index, to reduce the dimensionality of the dataframe
        df = df.stack(level=0)
        # stacking produces a series when I'm done, and it will need to be converted back into a DF
        df = df.to_frame()
        # now add a title to the DF's only column
        df.columns = ['great_smoky_mtns']
        # reset the index to seperate the current multi-index into distinct year and month columns
        df = df.reset_index(drop=False)
        # create a composite date column
        df['date'] = df.Year.astype(str) + "-" + df.level_1
        # convert the date column to datetime object
        df.date = pd.to_datetime(df.date)
        # set the date as the index and sort index
        df = df.set_index('date').sort_index()
        # drop Year and level_1 columns that are no longer needed
        df = df.drop(columns=['Year', 'level_1'])
        df.to_csv(filename, index=True)
        return df 

# 11. Get combined parks DataFrame:
def get_combined_park_visitors(use_cache=True):
    #use local cache from CSV if available
    filename = 'combined_park_visitors.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        yellowstone = prepare_yellowstone()
        grand_canyon = prepare_grand_canyon()
        rocky_mtn = prepare_rocky_mtn()
        zion = prepare_zion()
        great_smoky_mtns = prepare_great_smoky_mtns()
        # create combined df by merging df's on the date index
        combined_park_visitors = yellowstone.merge(grand_canyon, left_index=True, right_index=True, copy=True)
        combined_park_visitors = combined_park_visitors.merge(rocky_mtn,left_index=True, right_index=True, copy=True)
        combined_park_visitors = combined_park_visitors.merge(zion,left_index=True, right_index=True, copy=True)
        combined_park_visitors = combined_park_visitors.merge(great_smoky_mtns,left_index=True, right_index=True, copy=True)
        combined_park_visitors.to_csv(filename, index=False)
        return combined_park_visitors

# 12. Get final prepped and cleaned DataFrame
def cleaned_and_prepped_NPS_visitors():
    df = get_combined_park_visitors()
    df = df.drop(columns=['date_x', 'date_y', 'date_x.1', 'date_y.1'])
    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date).sort_index()
    df = df.drop(columns='date')
    # cleans the commas out of the numerical columns while they are strings. This only works if all the columns are string objects.
    df = df.apply(lambda x: x.str.replace(',', ''))
    #change columns from strings to int64
    df.yellowstone = df.yellowstone.astype('int64')
    df.grand_canyon = df.grand_canyon.astype('int64')
    df.rocky_mtn = df.rocky_mtn.astype('int64')
    df.zion = df.zion.astype('int64')
    df.great_smoky_mtns = df.great_smoky_mtns.astype('int64')
    return df
