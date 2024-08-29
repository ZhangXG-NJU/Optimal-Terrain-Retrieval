# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:39:46 2023

@author: Administrator
"""

import pandas as pd
import glob
from tqdm import tqdm

# Set the directory path
dirpath = r'D:\03_LPDEM\03_data\atl08\05_50val\step4.1_eachslope\555\\'

# Find all CSV files in the directory
csv_list = glob.glob(dirpath + '*.csv')
print('共发现%s个CSV文件' % len(csv_list))

# Initialize an empty list to store DataFrames
dfs = []

# Read each CSV file and store the DataFrame in the list
for i in tqdm(csv_list):
    data = pd.read_csv(i, encoding='utf-8')
    dfs.append(data)
print('合并完毕！')

# Concatenate all DataFrames in the list
df = pd.concat(dfs, ignore_index=True)

# Drop duplicate rows
df = df.drop_duplicates(keep='first')
print('去重完毕！')

# Save the concatenated DataFrame to a new CSV file
df.to_csv(r'D:\03_LPDEM\03_data\atl08\05_50val\step4.1_eachslope\555\test.csv', index=False, encoding="utf-8")
