import pandas as pd
import requests
import json
import os
import numpy as np
from variables import * # Importing all variables from the variables module
import time

start_time = time.time()  # start time of the script

"""Setting Key'"""
with open('config.json') as f:
    config = json.load(f)
key = config['key']

"""API Calls"""

# Due to  high volume of API calls and dataframes created, 
# calls to API are split in two groups:
#
# - Dataframes to be merged (get_vars, df_vars)
# - Dataframes to NOT merge (get_vars_A, df_vars_A)
#
# This will ease management since each type have many dissimilar features.

def fetch_data(url, how, where, get_vars, df_vars, key):
    """
    Fetches data from the specified URL using the given parameters.

    Parameters:
        url (str): The API endpoint URL.
        how (str): The 'how' parameter for the API call.
        where (str): The 'where' parameter for the API call.
        get_vars (list): The variables to retrieve.
        df_vars (list): The names of the DataFrames to create.
        key (str): The API key.

    Returns:
        dict: A dictionary containing DataFrames with the retrieved data.
    """
    dfs = {}  # Initialize an empty dictionary to store the DataFrames
    # Iterate through get_vars and df_vars
    for var, name in zip(get_vars, df_vars):
        # Set the parameters for the API call
        params = {
            "get": var,
            "for": where,
            "in": how,
            "key": key
        }
        r = requests.request('GET', url, params=params)  # Make the API call
        if r.status_code == 200:  # Check if the API call was successful
            data = r.json()
            df_data = data[1:]  # Extract the data from the JSON response
            dfs[name] = pd.DataFrame(df_data, columns=data[0])  # Create a DataFrame
            dfs[name]['FIPS'] = dfs[name]['state'] + dfs[name]['county']
            # Identify columns to convert to specific types
            columns_to_convert = ['NAME', 'state', 'county', 'FIPS']
            columns_to_convert = [
                col for col in columns_to_convert if col in dfs[name].columns
            ]
            # Convert selected columns to string type
            str_cols = dfs[name][columns_to_convert]
            dfs[name][columns_to_convert] = str_cols.astype(str)
            # Convert remaining columns to integer type
            int_cols = dfs[name][dfs[name].columns.difference(columns_to_convert)]
            dfs[name][int_cols.columns] = int_cols.astype(int)
        else:
            # Print an error message if the API call fails
            print(f"API call for '{var}' failed. Status code:", r.status_code)
    return dfs  # Return the dictionary of DataFrames

# Fetch data for dataframes to be merged
dfs = fetch_data(url, how, where, get_vars, df_vars, key)
# Fetch data for dataframes to NOT merge
dfs_A = fetch_data(url, how, where, get_vars_A, df_vars_A, key)

"""Merging Dataframes"""

# Merging dataframes based on name. Merged according to pattern in names.
# Example: 'DF_male_all' = 'DF_male_all_0' + 'DF_male_all_1' + 'DF_male_all_2'

# Create a dictionary to store the merged data frames
merged_dfs = {}

# Iterate over the items in the 'df_mrg' list to perform the merging
for item in df_mrg:
    # Create a list of dataframes to merge, dropping common columns
    dfs_to_merge = [df.drop(['NAME', 'state', 'county', 'FIPS'], axis=1) 
                    for df_name, df in dfs.items() if df_name.startswith(item)]
    
    # Merge by concat all columns; order based on 'df_mrg'
    merged_df = pd.concat(dfs_to_merge, axis=1, ignore_index=True)

    # Reset the index after concatenation
    merged_df = merged_df.reset_index(drop=True)
    
    # Add the common columns back to the merged data frame
    common_cols = ['NAME', 'state', 'county', 'FIPS']
    merged_df[common_cols] = dfs[item + '_0'][common_cols]
    
    # Add the merged data frame to the dictionary
    merged_dfs[item] = merged_df

"""Changing Column Names"""

# Changing column names to the dataframes in 'merged_dfs'

# Iterate over the items in the 'merged_dfs' dictionary
for item, df in merged_dfs.items():
    # Assign the new column names to the data frame in place
    df.columns = col_names
    # Update the data frame in the 'merged_dfs' dictionary
    merged_dfs[item] = df

"""Modify Column Locations"""

# Reindex columns to share column structure with merged dataframes.
# Specifically, we are swapping the first two columns so that the order becomes:
# ['NAME', 'state', 'county', 'FIPS']

# Iterate through the dataframes in the 'dfs_A' dictionary
for name, df in dfs_A.items():
    # Get the current list of columns
    columns = df.columns.tolist()
    
    # Swap the first two columns
    columns[0], columns[1] = columns[1], columns[0]
    
    # Reindex the dataframe with the modified column order
    df = df.reindex(columns=columns)
    
    # Update the dataframe in the 'dfs_A' dictionary with the new column order
    dfs_A[name] = df

"""Changing Column Names"""

# Changing column names to the dataframes in 'dfs_A'

col_names = ['Total','Location','State','County','FIPS']

# Iterate over the items in the 'dfs_A' dictionary
for item, df in dfs_A.items():
    df.columns = col_names  # Assign the new column names to dataframe in place
    dfs_A[item] = df  # Update the data frame in the 'dfs_A' dictionary

"""Merging"""

# 'merged_dfs' and 'dfs_A' using common keys from 'df_names'.
# Naming dataframes to match names in 'df_names' to ease .csv naming.

# Create an empty list to store the dataframes
df_export = []

# Iterate through the keys in df_names
for key in df_names:
    # Find the dataframe corresponding to the key in either merged_dfs or dfs_A
    if key in merged_dfs:
        df = merged_dfs[key]
    elif key in dfs_A:
        df = dfs_A[key]
    else:
        # Key not found in any dictionary
        print(f"Dataframe with key '{key}' not found in merged_dfs or dfs_A")
        continue

    # Assign the key as the name of the dataframe
    df.name = key

    # Append the dataframe to the df_export list
    df_export.append(df)

"""Create workbook and export wanted dataframes to excel as individual .csv."""

# Define the folder name
folder_name = 'age_sex_dataframes'

# Create the folder in the current working directory if it doesn't exist
folder_path = os.path.join(os.getcwd(), folder_name)
os.makedirs(folder_path, exist_ok=True)

# Iterate through the dataframes in df_export
for df in df_export:
    # Get the name of the dataframe
    name = df.name if hasattr(df, 'name') else 'Unnamed'
    
    # Define the CSV file name and path
    csv_file_name = f'{name}.csv'
    csv_file_path = os.path.join(folder_path, csv_file_name)

    # Save the DataFrame as a CSV file, overwriting if it already exists
    df.to_csv(csv_file_path, index=False)

end_time = time.time()  # end time of the script
# prints time taken to run the script
print(f'Time taken to run the entire script: {end_time - start_time} seconds')