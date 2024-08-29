import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# 读取CSV文件
df = pd.read_csv(r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\clipbuilding2.csv")
df.replace('None', np.nan, inplace=True)

df = df[df['year']==2022]

# 定义计算指标的函数
def calculate_metrics(y_true, y_pred):
    if len(y_true) < 2:
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    sd = np.std(y_true - y_pred)
    mean_error = np.mean(y_true - y_pred)
    nmad = np.median(np.abs(y_true - y_pred)) * 1.4826
    le90 = np.percentile(np.abs(y_true - y_pred), 90)
    return mean_error, mae, rmse, sd, nmad, r2, le90

# 读取区间权重文件
weights_df = pd.read_csv(r"D:\03_LPDEM\03_data\slo\slo_histogram.csv")

# 确保数据没有缺失值
error_columns = ['ast_dem', 'aw3_dem', 'cop_dem', 'fab_dem', 'nas_dem', 'srt_dem', 't30_dem', 'fus']
df.dropna(subset=error_columns, inplace=True)

true_values = df['lidar_egm']

# 按区间计算指标
interval_results = []
for i in range(68):
    interval_df = df[(df['slo_cop'] >= i) & (df['slo_cop'] < i + 1)]
    if not interval_df.empty and len(interval_df) >= 2:
        for col in error_columns:
            mean_error, mae, rmse, sd, nmad, r2, le90 = calculate_metrics(interval_df['lidar_egm'], interval_df[col])
            interval_results.append({
                'Interval': f"{i}-{i+1}",
                'DEM': col,
                'ME': mean_error,
                'MAE': mae,
                'RMSE': rmse,
                'SD': sd,
                'NMAD': nmad,
                'R²': r2,
                'LE90': le90
            })

interval_results_df = pd.DataFrame(interval_results)

# 加权计算整体指标
weighted_results = []
for col in error_columns:
    overall_metrics = {'ME': 0, 'MAE': 0, 'RMSE': 0, 'SD': 0, 'NMAD': 0, 'R²': 0, 'LE90': 0}
    total_weight = 0
    for i in range(69):
        weight = weights_df.loc[weights_df['Range Start'] == i, 'Percentage'].values
        if weight:
            interval_metrics = interval_results_df[(interval_results_df['Interval'] == f"{i}-{i+1}") & (interval_results_df['DEM'] == col)]
            if not interval_metrics.empty:
                for metric in overall_metrics.keys():
                    if not np.isnan(interval_metrics[metric].values[0]):
                        overall_metrics[metric] += interval_metrics[metric].values[0] * weight
                total_weight += weight
    if total_weight > 0:
        for metric in overall_metrics.keys():
            overall_metrics[metric] /= total_weight
    overall_metrics['DEM'] = col
    weighted_results.append(overall_metrics)

weighted_results_df = pd.DataFrame(weighted_results)

# 保存加权结果
weighted_results_df.to_csv(r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\Weighted_Metrics.csv", index=False)
