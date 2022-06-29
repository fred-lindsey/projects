

import pandas as pd
import requests
import os

#___________________________________________________________________________________________________________________
def get_sales_df(use_cache=True):
    #use local cache from CSV if available
    filename = "sales_df.csv"
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        #create empty list to store the pages
        sales = []

        #set the domain an endpoint
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/sales'

        # the url is the combination of domain and endpoint
        url = domain + endpoint

        #set the function parameters
        response = requests.get(url)
        data = response.json()

        # define the pages in the api
        current_page = data['payload']['page']
        next_page = data['payload']['next_page']
        max_page = data['payload']['max_page']

        # write a loop to run through 1: max page range
        for page in range (1, (max_page)):

            url_endpoint = data['payload']['next_page'] #use next page
            url = domain + url_endpoint

            # update the response to use the api next page to progress the script
            response = requests.get(url)
            data = response.json()

            # update the complete_sales_df to include the additional list items
            sales.extend(data['payload']['sales'])

            # check page progress with print statement
            print(f'\rFetching page {page} of {max_page} {url}', end='')
        sales = pd.DataFrame(sales)
        sales.to_csv(filename, index=False)
        # return the full dataframe
        return sales

#___________________________________________________________________________________________________________________
def get_items_df(use_cache=True):
    #use local cache from CSV if available
    filename = "items_df.csv"
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
    #create empty list to store the pages
        items = []

        #set the domain an endpoint
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/items'

        # the url is the combination of domain and endpoint
        url = domain + endpoint

        #set the function parameters
        response = requests.get(url)
        data = response.json()

        # define the pages in the api
        current_page = data['payload']['page']
        next_page = data['payload']['next_page']
        max_page = data['payload']['max_page']

        # write a loop to run through 1: max page range
        for page in range (1, (max_page)):

            endpoint = data['payload']['next_page'] #use next page
            url = domain + endpoint

            # update the response to use the api next page to progress the script
            response = requests.get(url)
            data = response.json()

            # update the complete_sales_df to include a concat of the additional dataframe
            items.extend(data['payload']['items'])

            # check page progress with print statement
            print(f'\rFetching page {page} of {max_page} {url}', end='')
        items = pd.DataFrame(items)
        items.to_csv(filename, index=False)
        # return the full dataframe
        return items

#___________________________________________________________________________________________________________________

def get_stores_df(use_cache=True):
    #use local cache from CSV if available
    filename = 'stores_df.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:

        #create empty list to store the pages
        stores = []

        #set the domain an endpoint
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/stores'

        # the url is the combination of domain and endpoint
        url = domain + endpoint

        #set the function parameters
        response = requests.get(url)
        data = response.json()

        # define the pages in the api
        current_page = data['payload']['page']
        next_page = data['payload']['next_page']
        max_page = data['payload']['max_page']
        print(max_page)

        # set URL:
        url = domain + endpoint

        # update the complete_sales_df to include a concat of the additional dataframe
        stores.extend(data['payload']['stores'])

        # check page progress with print statement
        print(f'\rFetching page {current_page} of {max_page} {url}', end='')
        stores = pd.DataFrame(stores)
        stores.to_csv(filename, index=False)
        # return the full dataframe
        return stores

#___________________________________________________________________________________________________________________

def get_combined_df(use_cache=True):
    #use local cache from CSV if available
    filename = 'combined_df.csv'
    if os.path.isfile(filename) and use_cache:
        return pd.read_csv(filename)
    else:
        sales_df = get_sales_df()
        items_df = get_items_df()
        stores_df = get_stores_df()
        combined_df = items_df.merge(sales_df, left_on='item_id', right_on='item', how='left', copy=False)
        combined_df = combined_df.merge(stores_df, left_on='store', right_on='store_id', how='left', copy=False)
        combined_df.to_csv(filename, index=False)
        return combined_df
