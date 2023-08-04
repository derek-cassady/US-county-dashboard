import pandas as pd
from openpyxl import workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np
import os
import xlsxwriter
# Importing all variables from the variables module
from variables import df_names,cols_int,cols_str,perc_df,perc_df_2,columns_to_drop

# Dictionary to store the dataframes
dfs = {}

# Get the path of the current working directory
cwd = os.getcwd()

# Construct the full path to the .xlsx file
file_path = os.path.join(cwd, '2020_agesex_data.xlsx')

# Load each sheet of the .xlsx file into a named dataframe
for name in df_names:
    df = pd.read_excel(file_path, sheet_name=name, header=None)
    df.columns = df.iloc[0]  # Set the first row as the column headers
    df = df[1:]  # Exclude the first row from the data
    df.reset_index(drop=True, inplace=True)  # Reset the index
    
    # Change column types based on column names
    for column in cols_int:
        if column in df.columns:
            df[column] = df[column].astype(int)
    
    for column in cols_str:
        if column in df.columns:
            df[column] = df[column].astype(str)
    
    dfs[name] = df


# ## Building Percent to Total column
# Percent to total for male & female age groups

# ### Grouping Dataframes with like structures

perc_df = ['DF_male_all','DF_female_all','DF_total_male_whi',
             'DF_total_female_whi','DF_total_male_baa','DF_total_female_baa',
             'DF_total_male_aian','DF_total_female_aian','DF_total_male_aa',
             'DF_total_female_aa','DF_total_male_nhop','DF_total_female_nhop',
             'DF_total_male_sor','DF_total_female_sor','DF_total_male_tom',
             'DF_total_female_tom','DF_total_male_hol','DF_total_female_hol'
             ]

perc_df_2 = ['DF_total_all','DF_total_whi','DF_total_baa','DF_total_aian',
             'DF_total_aa','DF_total_nhop','DF_total_sor','DF_total_tom',
             'DF_total_hol'
             ]


# Iterate over the dictionary of dataframes
for df_name, df in dfs.items():
    if df_name in perc_df:
        # Get the list of columns in the dataframe that match cols_int
        columns = [col for col in df.columns if col in cols_int]
        updated_columns = []

        # Reset the index to consolidate memory layout
        df.reset_index(drop=True, inplace=True)

        # Calculate the percentage values for the new column
        for col in columns:
            new_col_name = f'{col}_perc'
            updated_columns.extend([col, new_col_name])

            df[new_col_name] = [0 if total == 0 else (value / total)
                                for value, total in zip(df[col], df['Total'])]
        # Append ['Location', 'State', 'County', 'FIPS'] to updated_columns
        updated_columns.extend(['Total','Location', 'State', 'County', 'FIPS'])
        # Reorder the columns in the dataframe
        df = df[updated_columns]

        # Update the dataframe in the 'dfs' dictionary
        dfs[df_name] = df


# ## Building Weighted Average Column for 'perc_df' listed dfs

# Removing modified dataframes from dict dfs for further processing

# Initialize the new dictionary 'dfs_perc'
dfs_perc = {}

# Iterate over the dataframe names in 'perc_df' list
for df_name in perc_df:
    # Check if the dataframe name exists in 'dfs' dictionary
    if df_name in dfs:
        # Move the matching dataframe from 'dfs' to 'dfs_perc'
        dfs_perc[df_name] = dfs.pop(df_name)

# ### Variables for columns to drop to new dictionary

columns_to_drop = ['Under 1 Year_perc','1 Year_perc','2 Years_perc',
                  '3 Years_perc','4 Years_perc','5 Years_perc','6 Years_perc',
                  '7 Years_perc','8 Years_perc','9 Years_perc','10 Years_perc',
                  '11 Years_perc','12 Years_perc','13 Years_perc',
                  '14 Years_perc','15 Years_perc','16 Years_perc',
                  '17 Years_perc','18 Years_perc','19 Years_perc',
                  '20 Years_perc','21 Years_perc','22 Years_perc',
                  '23 Years_perc','24 Years_perc','25 Years_perc',
                  '26 Years_perc','27 Years_perc','28 Years_perc',
                  '29 Years_perc','30 Years_perc','31 Years_perc',
                  '32 Years_perc','33 Years_perc','34 Years_perc',
                  '35 Years_perc','36 Years_perc','37 Years_perc',
                  '38 Years_perc','39 Years_perc','40 Years_perc',
                  '41 Years_perc','42 Years_perc','43 Years_perc',
                  '44 Years_perc','45 Years_perc','46 Years_perc',
                  '47 Years_perc','48 Years_perc','49 Years_perc',
                  '50 Years_perc','51 Years_perc','52 Years_perc',
                  '53 Years_perc','54 Years_perc','55 Years_perc',
                  '56 Years_perc','57 Years_perc','58 Years_perc',
                  '59 Years_perc','60 Years_perc','61 Years_perc',
                  '62 Years_perc','63 Years_perc','64 Years_perc',
                  '65 Years_perc','66 Years_perc','67 Years_perc',
                  '68 Years_perc','69 Years_perc','70 Years_perc',
                  '71 Years_perc','72 Years_perc','73 Years_perc',
                  '74 Years_perc','75 Years_perc','76 Years_perc',
                  '77 Years_perc','78 Years_perc','79 Years_perc',
                  '80 Years_perc','81 Years_perc','82 Years_perc',
                  '83 Years_perc','84 Years_perc','85 Years_perc',
                  '86 Years_perc','87 Years_perc','88 Years_perc',
                  '89 Years_perc','90 Years_perc','91 Years_perc',
                  '92 Years_perc','93 Years_perc','94 Years_perc',
                  '95 Years_perc','96 Years_perc','97  Years_perc',
                  '98  Years_perc','99  Years_perc','100 to 104  Years_perc',
                  '105 to 109  Years_perc','110  Years and Over_perc','Total',
                  'Location','State','County','FIPS'
                  ]


dropped_columns = {}

# Iterate over the dataframes in 'dfs_perc'
for df_name, df in dfs_perc.items():
    # Store the dropped columns' data
    dropped_columns[df_name] = df[columns_to_drop]

    # Drop the specified columns from each dataframe
    dfs_perc[df_name] = df.drop(columns_to_drop, axis=1)

cols_mod = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
            25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,
            47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,
            69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,
            91,92,93,94,95,96,97,98,99,102,107,110
            ] 


# ### Column change process

# Iterate over the dataframes in 'dfs_perc'
for df_name, df in dfs_perc.items():
    # Change the column names to the list of integers
    df.columns = cols_mod
    
    # Convert the column type to integer
    df[cols_mod] = df[cols_mod].astype(int)


# ## Finding weighted Average

# Iterate over each key-value pair in dfs_perc
for df_name, df in dfs_perc.items():
    # Get the column names as an array of integers
    values = np.array(df.columns, dtype=int)

    # Initialize an empty list to store the results
    results = []

    # Iterate over each row in the dataframe
    for _, row in df.iterrows():
        # Get the row entries as an array of integers
        weights = np.array(row.values, dtype=int)

        # Perform element-wise multiplication of values and weights
        weighted_values = values * weights

        # Sum the products of the multiplications
        weighted_sum = np.sum(weighted_values)

        # Sum all items in the weights array
        weights_sum = np.sum(weights)

        # Calculate the weighted average
        weighted_average = weighted_sum / weights_sum

        # Append the weighted average to the results list
        results.append(weighted_average)

    # Add the 'Average_Age' column to the dataframe
    df['Average_Age'] = results

    # Reset the index of the dataframe
    df.reset_index(drop=True, inplace=True)

# ## Joining Dataframes

# Iterate over the dataframes in 'dfs_perc'
for df_name, df_perc in dfs_perc.items():
    # Get the corresponding dataframe from 'dropped_columns'
    df_dropped = dropped_columns[df_name]

    # Concatenate the dataframes width-wise
    joined_df = pd.concat([df_perc, df_dropped], axis=1)

    # Update the 'dfs_perc' dataframe in place with the joined dataframe
    dfs_perc[df_name] = joined_df

    # Reset the index of the dataframe
    dfs_perc[df_name].reset_index(drop=True, inplace=True)

# Delete the 'dropped_columns' dictionary to free up memory
del dropped_columns

# Selecting a specific dataframe to verify information has migrated correctly

# Merge the dictionaries 'dfs' and 'dfs_perc' into 'dfs' in the order of 'df_names'
for df_name in df_names:
    if df_name in dfs_perc:
        if df_name in dfs:
            df_merged = pd.concat([dfs[df_name], dfs_perc[df_name]], axis=1)
            dfs[df_name] = df_merged
        else:
            dfs[df_name] = dfs_perc[df_name]
# Delete the 'dfs_perc' dictionary to free up memory
del dfs_perc

# Create a dictionary to map the column prefixes to the corresponding dataframes
column_map = {
    'DF_total_all': ['DF_male_all', 'DF_female_all'],
    'DF_total_whi': ['DF_total_male_whi', 'DF_total_female_whi'],
    'DF_total_baa': ['DF_total_male_baa', 'DF_total_female_baa'],
    'DF_total_aian': ['DF_total_male_aian', 'DF_total_female_aian'],
    'DF_total_aa': ['DF_total_male_aa', 'DF_total_female_aa'],
    'DF_total_nhop': ['DF_total_male_nhop', 'DF_total_female_nhop'],
    'DF_total_sor': ['DF_total_male_sor', 'DF_total_female_sor'],
    'DF_total_tom': ['DF_total_male_tom', 'DF_total_female_tom'],
    'DF_total_hol': ['DF_total_male_hol', 'DF_total_female_hol']
}

# Copy 'Total' column to the correct dataframes
for key, value in column_map.items():
    # Slicing exclude the first three characters 'DF_'
    dfs[key][f'{value[0][3:]}'] = dfs[value[0]]['Total'].copy()
    dfs[key][f'{value[1][3:]}'] = dfs[value[1]]['Total'].copy()

# Create a dictionary to map the column prefixes to the corresponding dataframes
column_map = {
    'DF_total_all': ['DF_total_whi', 'DF_total_baa', 'DF_total_aian',
                     'DF_total_aa', 'DF_total_nhop', 'DF_total_sor',
                     'DF_total_tom', 'DF_total_hol'
                     ]}

# Copy 'Total' column to the correct dataframes
for key, value in column_map.items():
    for df_name in value:
        # Slicing exclude the first three characters 'DF_'
        dfs[key][df_name[3:]] = dfs[df_name]['Total'].copy()

# Create a dictionary to map the column prefixes to the corresponding dataframes
column_map = {
    'DF_total_all': ['DF_male_all', 'DF_female_all'],
    'DF_total_whi': ['DF_total_male_whi', 'DF_total_female_whi'],
    'DF_total_baa': ['DF_total_male_baa', 'DF_total_female_baa'],
    'DF_total_aian': ['DF_total_male_aian', 'DF_total_female_aian'],
    'DF_total_aa': ['DF_total_male_aa', 'DF_total_female_aa'],
    'DF_total_nhop': ['DF_total_male_nhop', 'DF_total_female_nhop'],
    'DF_total_sor': ['DF_total_male_sor', 'DF_total_female_sor'],
    'DF_total_tom': ['DF_total_male_tom', 'DF_total_female_tom'],
    'DF_total_hol': ['DF_total_male_hol', 'DF_total_female_hol']
}

# Iterate through the column_map to update other dataframes
    # Iterate through the columns in 'cols_mod'
for key, value in column_map.items():
    for column in cols_mod:
        dfs[key][column] = dfs[value[0]][column] + dfs[value[1]][column]

# Initialize the new dictionary 'dfs_perc_2'
dfs_perc_2 = {}

# Iterate over the dataframe names in 'perc_df_2' list
for df_name in perc_df_2:
    # Check if the dataframe name exists in 'dfs' dictionary
    if df_name in dfs:
        # Move a copy of the matching dataframe from 'dfs' to 'dfs_perc_2'
        dfs_perc_2[df_name] = dfs[df_name].copy()

# '''Dropping columns in list'cols_mod' to new dictionary.  Running weighted
# average arrays in new dict 'dropped_columns' then rejoining dictionaries to the
# affected dataframes from list 'perc_df_2'. I know, imagine how I feel, I'm the
# one writing the things.'''

dropped_columns = {}

# Iterate over the dataframes in dictionary 'dfs_perc_2'
    # Dataframe's name to 'df_name' and the dataframe itself to 'df'
for df_name, df in dfs_perc_2.items():
    # Store the dropped columns' data
        #dict[key] = only columns from list 'cols_mod'
    dropped_columns[df_name] = df[cols_mod]

    # Drop only columns from list 'cols_mod' each dataframe in dict 'dfs_perc_2'
    dfs_perc_2[df_name] = df.drop(cols_mod, axis=1)

# Iterate through the dataframes in 'dropped_columns' whose name is in list 'perc_df_2'
    # Dataframe's name to 'df_name' and the dataframe itself to 'df' in dict 'dropped_columns'
for df_name, df in dropped_columns.items():
    if df_name in perc_df_2:
        # Get the column names as an array of integers from 'cols_mod'
        values = np.array(cols_mod, dtype=int)

        # Initialize an empty list to store the results
        results = []

        # Iterate over each row in the dataframe
        for _, row in df.iterrows():
            # Get the row entries as an array of integers
            weights = np.array(row.values, dtype=int)

            # Perform element-wise multiplication of values and weights
            weighted_values = values * weights

            # Sum the products of the multiplications
            weighted_sum = np.sum(weighted_values)

            # Sum all items in the weights array
            weights_sum = np.sum(weights)

            # Calculate the weighted average, handle division by zero
            if weights_sum != 0:
                weighted_average = weighted_sum / weights_sum
            else:
                weighted_average = np.nan

            # Append the weighted average to the results list
            results.append(weighted_average)

        # Convert the results list to a float array explicitly
        results = np.array(results, dtype=float)

        # Add the 'Average_Age' column to the dataframe
        df['Average_Age'] = results

        # Reset the index of the dataframe
        df.reset_index(drop=True, inplace=True)

# ## Joining Dataframes

# Iterate through the dataframes in dict 'dfs_perc_2'
    # Dataframe's name to 'df_name' and the dataframe itself to 'df_perc' in dict 'dfs_perc_2'
for df_name, df_perc in dfs_perc_2.items():
    # Get the corresponding dataframe from 'dropped_columns'
    # Iterate through the dataframes in 'dfs_perc_2'
    df_dropped = dropped_columns[df_name]

    # Concatenate the dataframes width-wise
        # adding 104 columns to each dataframe, saving to var 'joined_df'
    joined_df = pd.concat([df_perc, df_dropped], axis=1)

    # Update the 'dfs_perc_2' dataframe in place with the joined dataframe
    dfs_perc_2[df_name] = joined_df

    # Reset the index of the dataframe
    dfs_perc_2[df_name].reset_index(drop=True, inplace=True)
# all data from weighted average now in dictionary of dataframes 'dfs_perc_2'
del dropped_columns

# Convert cols_mod to strings to iterate through properly
cols_mod_str = [str(col) for col in cols_mod]

# Create a new dictionary to store the modified dataframes
dfs_perc_2_updated = {}

# Iterate through each dataframe in the dictionary and change column names to type string
for key, df in dfs_perc_2.items():
    # Convert column names to strings
    df.columns = [str(col) for col in df.columns]

    # Create a copy of the original dataframe
    df_updated = df.copy()

    # Calculate the percentage values for the new columns
    for col in cols_mod_str:
        new_col_name = f'{col}_perc'
        df_updated[new_col_name] = [0 if total == 0 else (value / total)
                                    for value, total in zip(df[col], df['Total'])]

    # Add the updated dataframe to the new dictionary
    dfs_perc_2_updated[key] = df_updated

# Replace the original 'dfs_perc_2' dictionary with the updated one
dfs_perc_2 = dfs_perc_2_updated

# Function to cast column names to strings
def cast_column_names_to_string(df):
    df.columns = [str(col) for col in df.columns]
    return df

# Iterate through the dataframes in 'dfs' and 'dfs_perc_2' and cast column names to strings
for df_name, df in dfs.items():
    dfs[df_name] = cast_column_names_to_string(df)

for df_name, df in dfs_perc_2.items():
    dfs_perc_2[df_name] = cast_column_names_to_string(df)

# Merge the data from 'dfs_perc_2' into 'dfs'
for df_name, df_perc_2 in dfs_perc_2.items():
    # Check if the current dataframe exists in 'dfs'
    if df_name in dfs:
        # Get the original dataframe from 'dfs'
        df = dfs[df_name]

        # Check if there are any new columns in 'df_perc_2' that don't exist in 'df'
        new_columns = [col for col in df_perc_2.columns if col not in df.columns]

        # Add the new columns from 'df_perc_2' to 'df' without overwriting existing columns
        for col in new_columns:
            # Check for any duplicated columns and handle them if necessary
            new_col_name = col
            counter = 1
            while new_col_name in df.columns:
                new_col_name = f"{col}_{counter}"
                counter += 1

            df[new_col_name] = df_perc_2[col]

        # Update the dataframe in 'dfs' with the modified 'df'
        dfs[df_name] = df

# 'dfs' now contains the data from 'dfs_perc_2' with new columns added to the existing dataframes without overwriting existing columns

# Step 1: Calculate the expected total by summing the individual racial category columns
expected_total = dfs['DF_total_all'][['total_whi', 'total_baa', 'total_aian', 'total_aa', 'total_nhop', 'total_sor', 'total_tom', 'total_hol']].sum(axis=1)

# Step 2: Find the absolute error by subtracting the 'Total' column from the expected total
absolute_error = expected_total - dfs['DF_total_all']['Total']

# Step 3: Calculate the error rate as the absolute error divided by the expected total, multiplied by 100
error_rate = (absolute_error / expected_total) * 100

# Add the 'expected_total', 'absolute_error', and 'error_rate' columns to the DataFrame
dfs['DF_total_all']['Expected Total'] = expected_total
dfs['DF_total_all']['Absolute Error'] = absolute_error
dfs['DF_total_all']['Error Rate'] = error_rate


# ## Building Weighted Average Column for 'DF_total_all'

# Copy dataframe 'DF_total_all' from dict 'dfs' for further processing

# Loop through all the DataFrames in 'dfs' dictionary
for df_name, df in dfs.items():
    # Convert column names to strings
    df.columns = df.columns.astype(str)

    # Update the DataFrame in the 'dfs' dictionary
    dfs[df_name] = df


# The 'total all' DF is unique and needs to be done seperately

col_loc_tot_all = ['0','0_perc','1','1_perc','2','2_perc','3','3_perc','4','4_perc','5',
                   '5_perc','6','6_perc','7','7_perc','8','8_perc','9','9_perc','10',
                   '10_perc','11','11_perc','12','12_perc','13','13_perc','14',
                   '14_perc','15','15_perc','16','16_perc','17','17_perc','18',
                   '18_perc','19','19_perc','20','20_perc','21','21_perc','22',
                   '22_perc','23','23_perc','24','24_perc','25','25_perc','26',
                   '26_perc','27','27_perc','28','28_perc','29','29_perc','30',
                   '30_perc','31','31_perc','32','32_perc','33','33_perc','34',
                   '34_perc','35','35_perc','36','36_perc','37','37_perc','38',
                   '38_perc','39','39_perc','40','40_perc','41','41_perc','42',
                   '42_perc','43','43_perc','44','44_perc','45','45_perc','46',
                   '46_perc','47','47_perc','48','48_perc','49','49_perc','50',
                   '50_perc','51','51_perc','52','52_perc','53','53_perc','54',
                   '54_perc','55','55_perc','56','56_perc','57','57_perc','58',
                   '58_perc','59','59_perc','60','60_perc','61','61_perc','62',
                   '62_perc','63','63_perc','64','64_perc','65','65_perc','66',
                   '66_perc','67','67_perc','68','68_perc','69','69_perc','70',
                   '70_perc','71','71_perc','72','72_perc','73','73_perc','74',
                   '74_perc','75','75_perc','76','76_perc','77','77_perc','78',
                   '78_perc','79','79_perc','80','80_perc','81','81_perc','82',
                   '82_perc','83','83_perc','84','84_perc','85','85_perc','86',
                   '86_perc','87','87_perc','88','88_perc','89','89_perc','90',
                   '90_perc','91','91_perc','92','92_perc','93','93_perc','94',
                   '94_perc','95','95_perc','96','96_perc','97','97_perc','98',
                   '98_perc','99','99_perc','102','102_perc','107','107_perc',
                   '110','110_perc','Average_Age','male_all','female_all',
                   'total_whi','total_baa','total_aian','total_aa',
                   'total_nhop','total_sor','total_tom','total_hol',
                   'Expected Total','Total','Absolute Error','Error Rate',
                   'Location','State','County','FIPS'
                   ]

# Access the DataFrame in 'dfs' dictionary
df = dfs['DF_total_all']

# Reindex the DataFrame using the list
df = df.reindex(columns=col_loc_tot_all)

# Update the DataFrame in the 'dfs' dictionary
dfs['DF_total_all'] = df

# Inplace reset index to fix any fragmentation
df.reset_index(drop=True, inplace=True)


# ### Ordering process

# Setting the variables for column order for total race dataframes

df_perc_8 = ['DF_total_whi','DF_total_baa','DF_total_aian','DF_total_aa',
             'DF_total_nhop','DF_total_sor','DF_total_tom','DF_total_hol'
             ]

col_loc = ['0','0_perc','1','1_perc','2','2_perc','3','3_perc','4','4_perc','5','5_perc','6',
           '6_perc','7','7_perc','8','8_perc','9','9_perc','10','10_perc','11','11_perc',
           '12','12_perc','13','13_perc','14','14_perc','15','15_perc','16','16_perc','17',
           '17_perc','18','18_perc','19','19_perc','20','20_perc','21','21_perc','22',
           '22_perc','23','23_perc','24','24_perc','25','25_perc','26','26_perc','27',
           '27_perc','28','28_perc','29','29_perc','30','30_perc','31','31_perc','32',
           '32_perc','33','33_perc','34','34_perc','35','35_perc','36','36_perc','37',
           '37_perc','38','38_perc','39','39_perc','40','40_perc','41','41_perc','42',
           '42_perc','43','43_perc','44','44_perc','45','45_perc','46','46_perc','47',
           '47_perc','48','48_perc','49','49_perc','50','50_perc','51','51_perc','52',
           '52_perc','53','53_perc','54','54_perc','55','55_perc','56','56_perc','57',
           '57_perc','58','58_perc','59','59_perc','60','60_perc','61','61_perc','62',
           '62_perc','63','63_perc','64','64_perc','65','65_perc','66','66_perc','67',
           '67_perc','68','68_perc','69','69_perc','70','70_perc','71','71_perc','72',
           '72_perc','73','73_perc','74','74_perc','75','75_perc','76','76_perc','77',
           '77_perc','78','78_perc','79','79_perc','80','80_perc','81','81_perc','82',
           '82_perc','83','83_perc','84','84_perc','85','85_perc','86','86_perc','87',
           '87_perc','88','88_perc','89','89_perc','90','90_perc','91','91_perc','92',
           '92_perc','93','93_perc','94','94_perc','95','95_perc','96','96_perc','97',
           '97_perc','98','98_perc','99','99_perc','102','102_perc','107','107_perc',
           '110','110_perc','Average_Age','Total','Location','State','County',
           'FIPS']

spec_col_dict = {
        'DF_total_whi': ['total_male_whi','total_female_whi'],
        'DF_total_baa': ['total_male_baa','total_female_baa'],
        'DF_total_aian': ['total_male_aian','total_female_aian'],
        'DF_total_aa': ['total_male_aa','total_female_aa'],
        'DF_total_nhop': ['total_male_nhop','total_female_nhop'],
        'DF_total_sor': ['total_male_sor','total_female_sor'],
        'DF_total_tom': ['total_male_tom','total_female_tom'],
        'DF_total_hol': ['total_male_hol','total_female_hol'],
        }


# ### Ordering process

# Reorder the columns for each dataframe in 'df_perc_8'
for df_name in df_perc_8:
    # Get the dataframe from 'dfs'
    df = dfs[df_name]
    
    # Get the two unique columns specific to this dataframe
    unique_cols = spec_col_dict[df_name]
    
    # Get the columns that are not unique to this dataframe (common columns)
    common_cols = [col for col in col_loc if col not in unique_cols]
    
    # Calculate the number of columns that need to be inserted for each unique column
    num_cols_to_insert = len(common_cols)
    
    # Get the index where the unique columns should be inserted (index 207 in this case)
    insert_index = 207
    
    # Split the common columns into three groups to accommodate the insertion of unique columns
    common_cols_part1 = common_cols[:insert_index]
    common_cols_part2 = common_cols[insert_index:]
    
    # Reorder the columns as required
    df = df[common_cols_part1 + unique_cols + common_cols_part2]
    
    # Move the resulting dataframe back to the 'dfs' dictionary
    dfs[df_name] = df

# ## Export to excel

# Define the file name
file_name = '2020_agesex_statistics.xlsx'

# Get the file path in the current working directory
file_path = os.path.join(os.getcwd(), file_name)

# Always create a new workbook
writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

# Iterate through the dataframes in dfs
for df_name, df in dfs.items():  # Use 'dfs.items()' to get the name (key) and dataframe (value)
    # Get the name of the dataframe
    name = df_name

    # Write each dataframe to a separate sheet in the Excel file
    df.to_excel(writer, sheet_name=name, index=False)

# Close the writer
writer.close()

# Define the directory name
dir_name = 'Statistics_Dataframes'

# Get the directory path in the current working directory
dir_path = os.path.join(os.getcwd(), dir_name)

# Check if the directory exists, if not create it
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Iterate through the dataframes in dfs
for df_name, df in dfs.items():  # Use 'dfs.items()' to get the name (key) and dataframe (value)
    # Define the file name using the name of the dataframe
    file_name = f'{df_name}.xlsx'
    
    # Get the file path in the directory
    file_path = os.path.join(dir_path, file_name)
    
    # Write dataframe to a new Excel file using 'xlsxwriter' engine, overwrite if it already exists
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()