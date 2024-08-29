import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 设置Seaborn背景样式为darkgrid
sns.set(style="darkgrid")

# 读取CSV数据
data = pd.read_csv(r"D:\03_LPDEM\03_data\atl08\05_50val\step4_val\val.csv")

# 定义FHT区间
bins = list(range(0, 31, 2))  # 生成0到30，每隔2个单位的区间
labels = [f'{i}-{i+2}' for i in bins[:-1]]
data['fht_bin'] = pd.cut(data['fht'], bins=bins, labels=labels, include_lowest=True)

# 定义需要绘制箱线图的误差列，并进行倒序
error_columns = ['ast_err', 'aw3_err', 'cop_err', 'fab_err', 'nas_err', 'srt_err', 't30_err', 'fus_err']
titles = ['ASTER V3', 'AW3D30', 'COP30', 'FABDEM', 'NASADEM', 'SRTM V3', 'TAN30', 'OTRDEM']

# 创建结果DataFrame
results = []

palette = sns.color_palette("Greens", len(labels))
plt.figure(figsize=(18, 9))
gs = gridspec.GridSpec(2, 4, wspace=0.1, hspace=0.1)

for i, (col, title) in enumerate(zip(error_columns, titles)):
    ax = plt.subplot(2, 4, i+1)
    
    plt.axhline(0, color='red', linestyle='-', linewidth=1, zorder=0.5)
    
    sns.boxplot(x='fht_bin', y=col, data=data, fliersize=5, linewidth=1.5, showfliers=False, palette=palette)
    plt.title(f'{title}', fontsize=16, fontname='Times New Roman', fontweight='bold')
    plt.xticks(rotation=90, fontsize=12, fontname='Times New Roman')
    plt.yticks(fontsize=12, fontname='Times New Roman')
    
    if i < 4:
        plt.xlabel('')
    else:
        plt.xlabel('Canopy Height Interval (m)', fontsize=14, fontweight='bold', fontname='Times New Roman')
    if i % 4 != 0:
        plt.ylabel('')
    else:
        plt.ylabel('Error (m)', fontsize=14, fontweight='bold', fontname='Times New Roman')
    
    plt.ylim(-35, 75)
    
    # 计算每个fht_bin组的MAE和RMSE
    error_data = [data[data['fht_bin'] == label][col].dropna().values for label in labels]
    mae_data = [mean_absolute_error(array, np.zeros_like(array)) for array in error_data]
    rmse_data = [np.sqrt(mean_squared_error(array, np.zeros_like(array))) for array in error_data]
    mean_data = [np.mean(array) for array in error_data]
    le90_data = [np.percentile(np.abs(array), 90) for array in error_data]
    nmad_data = [1.4826 * np.median(np.abs(array - np.median(array))) for array in error_data]
    sd_data = [np.std(array) for array in error_data]
    
    # 添加MAE、RMSE和Mean到箱线图上
    for mae, rmse, mean, pos in zip(mae_data, rmse_data, mean_data, np.arange(0, len(labels))):
        plt.scatter(pos, mae, c='orange', marker='o', zorder=10, s=20, label='MAE' if pos == 1 else "")
        plt.scatter(pos, rmse, c='royalblue', marker='^', zorder=10, s=23, label='RMSE' if pos == 1 else "")
        plt.scatter(pos, mean, c='red', marker='x', zorder=10, s=25, label='Mean' if pos == 1 else "")
    
    # 保存结果到DataFrame
    for label, mae, rmse, mean, le90, nmad, sd in zip(labels, mae_data, rmse_data, mean_data, le90_data, nmad_data, sd_data):
        results.append([title, label, mae, rmse, mean, le90, nmad, sd])
    
    # 设置灰色部分的黑色框，宽度1.5
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)
    
    # 调整 xticks 和 yticks 更靠近主图，并显示触须
    ax.tick_params(pad=1)

# 减小子图之间的间距
plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
plt.savefig(r"D:\03_LPDEM\05_figures\Figure10 FHT Val\FHT_Boxplot.svg", dpi=1200)
plt.show()

# 创建结果DataFrame并保存为CSV
results_df = pd.DataFrame(results, columns=['Dataset', 'Canopy Height Interval', 'MAE', 'RMSE', 'Mean', 'LE90', 'NMAD', 'SD'])
results_df.to_csv(r"D:\03_LPDEM\05_figures\FHT_Validation_Results.csv", index=False)

print("结果已保存到CSV文件中。")
