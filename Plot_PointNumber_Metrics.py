# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:25:17 2024

@author: Zhang Xin-Gang
"""

import matplotlib.pyplot as plt
import pandas as pd

# Set the font globally to Times New Roman, bold
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["font.size"] = "14"

path = r"D:\17_LPDEM\07_outputs\03_pnumber\merged_results\Statistic.csv"

df = pd.read_csv(path)

fig, ax1 = plt.subplots(figsize=(14, 4))

color = 'tab:blue'
ax1.plot(df['Number'], df['RMSE'], marker='o', color=color, label='RMSE')
# ax1.set_ylabel('RMSE', color=color, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(axis='y', linestyle='-', linewidth=0.5)  # Only vertical grid lines

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.plot(df['Number'], df['MAE'], marker='s', color=color, label='MAE')
# ax2.set_ylabel('MAE', color=color, fontweight='bold')  # we already handled the x-label with ax1
ax2.tick_params(axis='y', labelcolor=color)

# Remove Y-axis labels
ax1.yaxis.set_label_coords(-0.1, 0.5)
ax2.yaxis.set_label_coords(1.1, 0.5)

ax1.set_xticks(range(0, 110, 10))
ax1.set_xlabel('Selected Nearest Point Number', fontweight='bold')

ax1.set_yticks([3.24, 3.27, 3.30, 3.33, 3.36, 3.39, 3.42])
ax2.set_yticks([1.515, 1.52, 1.525, 1.53, 1.535, 1.54, 1.545, 1.55, 1.555])

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# Add legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.savefig(r'D:\03_LPDEM\05_figures\Figure11 pnumber\Step3_MAE&RMSE\MAE_RMSE_Changes.svg')
plt.show()
