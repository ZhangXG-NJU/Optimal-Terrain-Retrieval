import os
import glob
import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import box

# Configure matplotlib to use Times New Roman font
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.unicode_minus': False
})

# 获取文件夹中所有GeoTIFF文件
folder_path = r"D:\03_LPDEM\05_figures\Figure12 FindError\111"
tif_files = glob.glob(os.path.join(folder_path, "*.tif"))

# 创建输出文件夹
output_folder = os.path.join(folder_path, "output_images")
os.makedirs(output_folder, exist_ok=True)

# 循环处理每个GeoTIFF文件
for tif_file in tif_files:
    # 读取GeoTIFF文件
    dataset = rasterio.open(tif_file)

    # 读取地理坐标范围
    minx, miny, maxx, maxy = dataset.bounds

    # 计算经纬度范围的4等分点
    x_ticks = [minx + (i + 0.5) * (maxx - minx) / 2 for i in range(2)]
    y_ticks = [miny + (i + 0.5) * (maxy - miny) / 2 for i in range(2)]

    # 创建地理边框
    geometry = box(minx, miny, maxx, maxy)
    gdf = gpd.GeoDataFrame(geometry=[geometry], crs=dataset.crs)

    # 读取RGB波段
    img = dataset.read([1, 2, 3], masked=True)

    # 处理透明区域，设置透明区域为白色
    mask = img.mask.any(axis=0)
    img = img.filled(255)  # 将掩模区域填充为白色

    # 将图像维度转换为绘图格式
    img = img.transpose((1, 2, 0))

    # 绘制图像
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img, extent=[minx, maxx, miny, maxy], cmap='viridis')

    # 设置背景颜色为白色
    ax.set_facecolor('white')

    # 添加地理边框
    gdf.boundary.plot(ax=ax, edgecolor='black', linewidth=5)

    # 添加经纬度标注
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis='both', direction='in', width=5, length=10)
    ax.set_xticklabels([f"{tick:.3f}°E" for tick in x_ticks], fontsize=28)
    ax.set_yticklabels([f"{tick:.3f}°N" for tick in y_ticks], fontsize=28, rotation='vertical', verticalalignment='center')

    ax.set_aspect('equal')

    # 保存图像
    output_file = os.path.join(output_folder, f"{os.path.basename(tif_file)[:-4]}.png")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, facecolor='white')
    plt.close()

print("图像处理完成，并保存到输出文件夹。")
