# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import pandas as pd

# Load the CSV file
df = pd.read_csv(r"E:\Zhang_XinGang\17_LPDEM\03_data\atl08\02_withDEMs\atl08_withDEMs.csv")

# Define a function to check if absolute values are greater than 50 for a row
def is_bad_photon(row):
    errors = ["ast_err", "aw3_err", "cop_err", "fab_err", "nas_err", "srt_err", "t30_err"]
    return all(abs(row[error]) > 50 for error in errors)

# Apply the function to create a new column 'is_bad' indicating whether it's a bad photon
df['is_bad'] = df.apply(is_bad_photon, axis=1)

# Split the dataframe into Good and Bad photons
good_photons = df[df['is_bad'] == False]
bad_photons = df[df['is_bad'] == True]

# Save the data to separate CSV files
good_photons.to_csv(r"..\03_data\atl08\03_Photonfilt\Good_Photons.csv", index=False)
bad_photons.to_csv(r"..\03_data\atl08\03_Photonfilt\Bad_Photons.csv", index=False)
