import pandas as pd
from openpyxl import workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np
import os
import math

# Creating ordered list of DFs to name each sheet coming in from workbook
df_names = ['DF_total_all','DF_male_all','DF_female_all','DF_total_whi',
            'DF_total_male_whi','DF_total_female_whi','DF_total_baa',
            'DF_total_male_baa','DF_total_female_baa','DF_total_aian',
            'DF_total_male_aian','DF_total_female_aian','DF_total_aa',
            'DF_total_male_aa','DF_total_female_aa','DF_total_nhop',
            'DF_total_male_nhop','DF_total_female_nhop','DF_total_sor',
            'DF_total_male_sor','DF_total_female_sor','DF_total_tom',
            'DF_total_male_tom','DF_total_female_tom','DF_total_hol',
            'DF_total_male_hol','DF_total_female_hol'
            ]

cols_int = ['Under 1 Year','1 Year','2 Years','3 Years','4 Years','5 Years',
            '6 Years','7 Years','8 Years','9 Years','10 Years','11 Years',
            '12 Years','13 Years','14 Years','15 Years','16 Years','17 Years',
            '18 Years','19 Years','20 Years','21 Years','22 Years','23 Years',
            '24 Years','25 Years','26 Years','27 Years','28 Years','29 Years',
            '30 Years','31 Years','32 Years','33 Years','34 Years','35 Years',
            '36 Years','37 Years','38 Years','39 Years','40 Years','41 Years',
            '42 Years','43 Years','44 Years','45 Years','46 Years','47 Years',
            '48 Years','49 Years','50 Years','51 Years','52 Years','53 Years',
            '54 Years','55 Years','56 Years','57 Years','58 Years','59 Years',
            '60 Years','61 Years','62 Years','63 Years','64 Years','65 Years',
            '66 Years','67 Years','68 Years','69 Years','70 Years','71 Years',
            '72 Years','73 Years','74 Years','75 Years','76 Years','77 Years',
            '78 Years','79 Years','80 Years','81 Years','82 Years','83 Years',
            '84 Years','85 Years','86 Years','87 Years','88 Years','89 Years',
            '90 Years','91 Years','92 Years','93 Years','94 Years','95 Years',
            '96 Years','97  Years','98  Years','99  Years','100 to 104  Years',
            '105 to 109  Years','110  Years and Over'
            ]

cols_str = ['Location', 'State', 'County', 'FIPS']

# Dictionary to store the dataframes
dfs = {}

# Get the path of the current working directory
cwd = os.getcwd()

# Construct the full path to the .xlsx file
file_path = os.path.join(cwd, '2020_agesex_data.xlsx')

# Load each sheet of the .xlsx file into a named dataframe
for name in df_names:
    df = pd.read_excel(file_path, sheet_name=name, header=None)  # Specify header=None to treat the first row as data
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

            df[new_col_name] = [0 if total == 0 else (value / total) * 100
                                for value, total in zip(df[col], df['Total'])]
        # Append ['Location', 'State', 'County', 'FIPS'] to updated_columns
        updated_columns.extend(['Total','Location', 'State', 'County', 'FIPS'])
        # Reorder the columns in the dataframe
        df = df[updated_columns]

        # Update the dataframe in the 'dfs' dictionary
        dfs[df_name] = df

new_cols = ['Under 1 Year','Under 1 Year_perc','1 Year','1 Year_perc',
            '2 Years','2 Years_perc','3 Years','3 Years_perc','4 Years',
            '4 Years_perc','5 Years','5 Years_perc','6 Years','6 Years_perc',
            '7 Years','7 Years_perc','8 Years','8 Years_perc','9 Years',
            '9 Years_perc','10 Years','10 Years_perc','11 Years',
            '11 Years_perc','12 Years','12 Years_perc','13 Years',
            '13 Years_perc','14 Years','14 Years_perc','15 Years',
            '15 Years_perc','16 Years','16 Years_perc','17 Years',
            '17 Years_perc','18 Years','18 Years_perc','19 Years',
            '19 Years_perc','20 Years','20 Years_perc','21 Years',
            '21 Years_perc','22 Years','22 Years_perc','23 Years',
            '23 Years_perc','24 Years','24 Years_perc','25 Years',
            '25 Years_perc','26 Years','26 Years_perc','27 Years',
            '27 Years_perc','28 Years','28 Years_perc','29 Years',
            '29 Years_perc','30 Years','30 Years_perc','31 Years',
            '31 Years_perc','32 Years','32 Years_perc','33 Years',
            '33 Years_perc','34 Years','34 Years_perc','35 Years',
            '35 Years_perc','36 Years','36 Years_perc','37 Years',
            '37 Years_perc','38 Years','38 Years_perc','39 Years',
            '39 Years_perc','40 Years','40 Years_perc','41 Years',
            '41 Years_perc','42 Years','42 Years_perc','43 Years',
            '43 Years_perc','44 Years','44 Years_perc','45 Years',
            '45 Years_perc','46 Years','46 Years_perc','47 Years',
            '47 Years_perc','48 Years','48 Years_perc','49 Years',
            '49 Years_perc','50 Years','50 Years_perc','51 Years',
            '51 Years_perc','52 Years','52 Years_perc','53 Years',
            '53 Years_perc','54 Years','54 Years_perc','55 Years',
            '55 Years_perc','56 Years','56 Years_perc','57 Years',
            '57 Years_perc','58 Years','58 Years_perc','59 Years',
            '59 Years_perc','60 Years','60 Years_perc','61 Years',
            '61 Years_perc','62 Years','62 Years_perc','63 Years',
            '63 Years_perc','64 Years','64 Years_perc','65 Years',
            '65 Years_perc','66 Years','66 Years_perc','67 Years',
            '67 Years_perc','68 Years','68 Years_perc','69 Years',
            '69 Years_perc','70 Years','70 Years_perc','71 Years',
            '71 Years_perc','72 Years','72 Years_perc','73 Years',
            '73 Years_perc','74 Years','74 Years_perc','75 Years',
            '75 Years_perc','76 Years','76 Years_perc','77 Years',
            '77 Years_perc','78 Years','78 Years_perc','79 Years',
            '79 Years_perc','80 Years','80 Years_perc','81 Years',
            '81 Years_perc','82 Years','82 Years_perc','83 Years',
            '83 Years_perc','84 Years','84 Years_perc','85 Years',
            '85 Years_perc','86 Years','86 Years_perc','87 Years',
            '87 Years_perc','88 Years','88 Years_perc','89 Years',
            '89 Years_perc','90 Years','90 Years_perc','91 Years',
            '91 Years_perc','92 Years','92 Years_perc','93 Years',
            '93 Years_perc','94 Years','94 Years_perc','95 Years',
            '95 Years_perc','96 Years','96 Years_perc','97  Years',
            '97  Years_perc','98  Years','98  Years_perc','99  Years',
            '99  Years_perc','100 to 104  Years','100 to 104  Years_perc',
            '105 to 109  Years','105 to 109  Years_perc','110  Years and Over',
            '110  Years and Over_perc','Total','Location','State','County','FIPS'
            ]

col_names = ['0','115','1','1115','2','2115','3','3115','4',
             '4115','5','5115','6','6115','7','7115','8','8115','9',
             '9115','10','10115','11','11115','12','12115','13',
             '13115','14','14115','15','15115','16','16115','17',
             '17115','18','18115','19','19115','20','20115','21',
             '21115','22','22115','23','23115','24','24115','25',
             '25115','26','26115','27','27115','28','28115','29',
             '29115','30','30115','31','31115','32','32115','33',
             '33115','34','34115','35','35115','36','36115','37',
             '37115','38','38115','39','39115','40','40115','41',
             '41115','42','42115','43','43115','44','44115','45',
             '45115','46','46115','47','47115','48','48115','49',
             '49115','50','50115','51','51115','52','52115','53',
             '53115','54','54115','55','55115','56','56115','57',
             '57115','58','58115','59','59115','60','60115','61',
             '61115','62','62115','63','63115','64','64115','65',
             '65115','66','66115','67','67115','68','68115','69',
             '69115','70','70115','71','71115','72','72115','73',
             '73115','74','74115','75','75115','76','76115','77',
             '77115','78','78115','79','79115','80','80115','81',
             '81115','82','82115','83','83115','84','84115','85',
             '85115','86','86115','87','87115','88','88115','89',
             '89115','90','90115','91','91115','92','92115','93',
             '93115','94','94115','95','95115','96','96115','97',
             '97115','98','98115','99','99115','102','102115','107',
             '107115','110','110115','Total','Location','State','County','FIPS'
             ]

col_ints = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','102','107','110']

col_strings = ['0_perc','1_perc','2_perc','3_perc','4_perc','5_perc',
               '6_perc','7_perc','8_perc','9_perc','10_perc','11_perc',
               '12_perc','13_perc','14_perc','15_perc','16_perc','17_perc',
               '18_perc','19_perc','20_perc','21_perc','22_perc','23_perc',
               '24_perc','25_perc','26_perc','27_perc','28_perc','29_perc',
               '30_perc','31_perc','32_perc','33_perc','34_perc','35_perc',
               '36_perc','37_perc','38_perc','39_perc','40_perc','41_perc',
               '42_perc','43_perc','44_perc','45_perc','46_perc','47_perc',
               '48_perc','49_perc','50_perc','51_perc','52_perc','53_perc',
               '54_perc','55_perc','56_perc','57_perc','58_perc','59_perc',
               '60_perc','61_perc','62_perc','63_perc','64_perc','65_perc',
               '66_perc','67_perc','68_perc','69_perc','70_perc','71_perc',
               '72_perc','73_perc','74_perc','75_perc','76_perc','77_perc',
               '78_perc','79_perc','80_perc','81_perc','82_perc','83_perc',
               '84_perc','85_perc','86_perc','87_perc','88_perc','89_perc',
               '90_perc','91_perc','92_perc','93_perc','94_perc','95_perc',
               '96_perc','97_perc','98_perc','99_perc','102_perc','107_perc',
               '110_perc','Total','Location','State','County','FIPS'
               ]

# Iterate over the dataframes in 'dfs'
for key, df in dfs.items():
    # Check if the dataframe is present in 'perc_df'
    if key in perc_df:
        # Modify column names based on 'col_names' list
        df.columns = col_names[:len(df.columns)]

        # # Loop through the columns to convert to integers
        # for col in df.columns:
        #     if col in col_ints:
        #         # Change the column name to an integer
        #         df.rename(columns={col: int(col)}, inplace=True)
        #         # Convert the column values to integers
        #         df[int(col)] = df[int(col)].astype(int)

        for col_index, col_name in enumerate(df.columns):
            if 0 <= col_index <= 205:
                # Convert column name to integer
                col_number = int(col_name)
                # Assign the new integer column name
                df.rename(columns={col_name: col_number}, inplace=True)

# Reset the index to a simple range index
df = df.reset_index(drop=True)

# Iter df dict for df in perc_df 
for df_name, df in dfs.items():
    if df_name in perc_df:
        # Drop columns 'Total', 'Location', 'State', 'County', and 'FIPS'
        df = df.drop(columns=['Total', 'Location', 'State', 'County', 'FIPS'])

        # Insert an empty column at index 0
        # Allows for slicing from col[0]
        df.insert (0,999,0)

        # Convert the new column to int type
        # Needs to be the same as the other columns
        df[df.columns[0]] = df[df.columns[0]].astype(int)

        # This is why we added the new column
        # Select columns 0 to 102 (inclusive) with a step of 2
        values_columns = df.columns[0:206:1]
        # Select columns 1 to 103 (inclusive) with a step of 2
        weights_columns = df.columns[1:206:2]

        # Create empty lists to store stages of weighted average equation
        numerator = []
        denominator = []

        # Inside of our while loop for dfs in perc_df:
        # Iterate through the variables 1:1
        i = 0

        while i < len(values_columns) and i < len(weights_columns):
            value = values_columns[i]
            weight = weights_columns[i]
    
            # Each iteration creates a product
            product = value * weight
    
            # Each iteration product stored in the numerator list 
            numerator.append(product)
            
            # Counter to keep track of the current iteration
            i += 1
        
        while i < len(weights_columns):
            weight = weights_columns[i]

            # Each iteration product stored in the numerator list 
            denominator.append(product)

            # Counter to keep track of the current iteration
            i += 1

        weighted_average = sum(numerator) / sum(denominator)   