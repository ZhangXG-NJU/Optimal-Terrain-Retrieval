# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import glob
import pandas as pd
from tqdm import tqdm

def get_part(filename):
    return filename.split("\\")[6].split("_")[0]

merged_df = pd.DataFrame()


path  = r"E:\Zhang_XinGang\17_LPDEM\03_data\atl08\01_raw\8\*.csv"
files = glob.glob(path)

for file in tqdm(files):
    df = pd.read_csv(file)
    part = get_part(file)
    df["granule"] = part
    merged_df = merged_df.append(df)

merged_df.to_csv(r"E:\Zhang_XinGang\17_LPDEM\03_data\atl08\01_raw\atl08_8.csv", index=False)
