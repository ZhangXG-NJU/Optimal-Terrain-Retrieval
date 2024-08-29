# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import pandas as pd

# Load the CSV file
file_path = r"D:\03_LPDEM\03_data\gedi\06_50val\gedi_11.csv"
df = pd.read_csv(file_path)

# Define the fields to subtract
fields_to_subtract = ['step1_fus']

# Convert relevant columns to numeric
numeric_columns = ['lidar_egm'] + fields_to_subtract
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Loop through the fields and subtract their values
for field in fields_to_subtract:
    new_field_name = field + '_err'
    df[new_field_name] = df[field] - df['lidar_egm']
    df[new_field_name] = df[new_field_name].round(2)
    print(str(new_field_name) + " finished.")

# Save the modified DataFrame back to a CSV file
output_path = r"D:\03_LPDEM\03_data\gedi\06_50val\2gedi_11.csv"
df.to_csv(output_path, index=False)




