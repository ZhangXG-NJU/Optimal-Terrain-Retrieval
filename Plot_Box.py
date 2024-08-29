import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from matplotlib.cm import get_cmap

# 设置绘图样式
sns.set(font="Times New Roman", font_scale=1.1, style="darkgrid")

# 读取数据文件
file_path = r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\clipbuilding.csv"
df = pd.read_csv(file_path)

# 定义变量
error_cols  = ['fus_err', 't30_err', 'srt_err', 'nas_err', 'fab_err', 'cop_err', 'aw3_err', 'ast_err' ]
error_names = ['OTRDEM' , 'TAN30'  , 'SRTM V3', 'NASADEM', 'FABDEM' , 'COP30'  , 'AW3D30' , 'ASTER V3']
facecolors  = ['#454545', '#7A0403', '#E3440A', '#FBB938', '#A4FC3C', '#1BE5B5', '#4686FB', '#30123B']

# 处理数据
error_data  = [df[col].dropna().values for col in error_cols]

# 创建绘图并进行配置
plt.figure(figsize=(6.5, 4.33333333333333333333))
plt.axvline(x=0, color='white', linestyle='-', linewidth=2)

# 绘制箱线图
bp = plt.boxplot(error_data,
                 vert=False,
                 widths=0.65,
                 patch_artist=True,
                 positions=np.arange(1, len(error_cols) + 1),
                 showfliers=False,
                 showmeans=True,
                 meanprops = {'marker':'x','markerfacecolor':'None','markeredgecolor':'black',},
                 medianprops = {'linestyle':'-','color':'black'},
                 )

# 设置箱线图颜色和线条宽度
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(color = facecolors[i])
    box.set_alpha(0.75)
    bp['caps'][i*2].set_linewidth(1.0) 
    bp['caps'][i*2+1].set_linewidth(1.0)

# 设置y轴刻度和网格
plt.yticks(np.arange(1, len(error_cols) + 1), error_names)
plt.grid(axis='y')
plt.xlim(-8, 8)
plt.xticks([-7.5, -5, -2.5, 0, 2.5, 5, 7.5], fontsize=15, fontweight='bold')

# 使 y 轴标签加粗
ax = plt.gca()
ax.set_yticklabels(error_names, fontweight='bold')

# 使 OTRDEM 标签变为红色
for label in ax.get_yticklabels():
    if 'OTR' in label.get_text():
        label.set_color('red')

# 计算MAE和RMSE数据并添加到图中
mae_data  = [mean_absolute_error(array, np.zeros_like(array)) for array in error_data]
rmse_data = [np.sqrt(mean_squared_error(array, np.zeros_like(array))) for array in error_data]

for mae, rmse, pos in zip(mae_data, rmse_data, np.arange(1, len(error_cols) + 1)):
    plt.scatter(mae, pos, c='black', marker='o', zorder=10, s=20)
    plt.scatter(rmse, pos, c='black', marker='^', zorder=10, s=23)

# 设置x轴标签
plt.xlabel('Error (m)', fontsize=15, fontweight='bold')

# 获取当前的Axes对象并设置边框
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(1)

plt.tight_layout()
plt.savefig(r'D:\03_LPDEM\05_figures\Figure8 MainVal\Box.svg',dpi=600)

# 显示绘图
plt.show()
