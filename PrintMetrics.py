# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

df = pd.read_csv(r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\clipbuilding.csv")

df.replace('None', np.nan, inplace=True)

def calculate_metrics(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    sd = np.std(y_true - y_pred)
    mean_error = np.mean(y_true - y_pred)
    nmad = np.median(np.abs(y_true - y_pred)) * 1.4826
    le90 = np.percentile(np.abs(y_true - y_pred), 90)
    return mean_error, mae, rmse, sd, nmad, r2, le90

error_columns = ['ast_dem', 'aw3_dem', 'cop_dem', 'fab_dem', 'nas_dem', 'srt_dem', 't30_dem', 'fus']
df.dropna(subset=error_columns, inplace=True)

true_values = df['lidar_egm']

results = []

for col in error_columns:
    mean_error, mae, rmse, sd, nmad, r2, le90 = calculate_metrics(true_values, df[col])
    results.append({
        'DEM': col,
        'ME': mean_error,
        'MAE': mae,
        'RMSE': rmse,
        'SD': sd,
        'NMAD': nmad,
        'R²': r2,
        'LE90': le90
    })

results_df = pd.DataFrame(results)
results_df.to_csv(r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\metrics_results.csv", index=False)
print(results_df)
print("Results saved to metrics_results.csv")