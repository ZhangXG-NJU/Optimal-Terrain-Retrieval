import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.cm import get_cmap

file_path = r"D:\03_LPDEM\03_data\atl08\05_50val\step3_clipbuilding\clipbuilding.csv"
df = pd.read_csv(file_path)

facecolors  = ['#30123B', '#4686FB', '#1BE5B5', '#A4FC3C', '#FBB938', '#E3440A', '#7A0403', '#454545']
error_names = ['ASTER V3', 'AW3D30', 'COP30', 'FABDEM', 'NASADEM', 'SRTM V3', 'TAN30', 'OTRDEM']
error_cols  = ['ast_err', 'aw3_err', 'cop_err', 'fab_err', 'nas_err', 'srt_err', 't30_err', 'fus_err']

# 绘制直方图
sns.set(font="Times New Roman", font_scale=1.5, style="darkgrid")
fig, axes = plt.subplots(2, 4, figsize=(12, 10))  # 两行四列
plt.subplots_adjust(wspace=0.3, hspace=0.4)

# 遍历每个误差列
for i, error_col in enumerate(error_cols):
    row = i // 4  # 确定子图的行
    col = i % 4   # 确定子图的列
    error_name = error_names[i]  # 确定误差名称
    color = facecolors[i]  # 确定颜色
    error_data = df[error_col].values  # 提取误差数据
    sns.histplot(x=error_data, ax=axes[row, col], bins='auto', stat='count', color=color, binwidth=0.1, alpha=0.75)  # 绘制直方图
    axes[row, col].set_title(error_name, fontsize=22, fontweight='bold', pad=10)  # 设置标题
    axes[row, col].set_xlabel('Error (m)', fontsize=21, fontweight='bold')
    axes[row, col].set_ylabel('Point Number', fontsize=21, fontweight='bold')  # 设置y轴标签
    axes[row, col].tick_params(axis='both', labelsize=21)  # 设置刻度参数
    axes[row, col].spines['top'].set_color('black')
    axes[row, col].spines['bottom'].set_color('black')
    axes[row, col].spines['left'].set_color('black')
    axes[row, col].spines['right'].set_color('black')
    axes[row, col].spines['top'].set_linewidth(1.5)
    axes[row, col].spines['bottom'].set_linewidth(1.5)
    axes[row, col].spines['left'].set_linewidth(1.5)
    axes[row, col].spines['right'].set_linewidth(1.5)
    
    # 隐藏除了最左边的子图的y轴标签和刻度
    if col != 0:
        axes[row, col].tick_params(axis='y', which='both', left=False, labelleft=False)
        axes[row, col].set_ylabel('')
    if row == 0:
        axes[row, col].set_xlabel('')

# 设置所有子图的相同的x和y轴范围
xmin, xmax = -5, 5
ymin, ymax = 0, 1260000
for ax in axes.flat:
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

# 调整布局并保存图像
plt.tight_layout()
plt.savefig(r'D:\03_LPDEM\05_figures\Figure8 MainVal\Histogram.svg')
plt.show()
