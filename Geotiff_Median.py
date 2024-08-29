# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 20:19:46 2023

@author: Administrator
"""

import numpy as np
from Geotiff_read_write import ReadGeoTiff, GetGeoInfo, CreateGeoTiff

ast_arr, ast_Ysize, ast_Xsize = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_ast.tif")
aw3_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_aw3.tif")
cop_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_cop.tif")
fab_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_fab.tif")
mrt_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_mrt.tif")
nas_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_nas.tif")
srt_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_srt.tif")
tan_arr,_,_ = ReadGeoTiff(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_tan.tif")

GeoT, Projection = GetGeoInfo(r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo_ast.tif")

# 使用np.stack函数将多个矩阵堆叠成一个三维数组
matrices = np.stack([ast_arr, aw3_arr, cop_arr, fab_arr, mrt_arr, nas_arr, srt_arr])

del ast_arr, aw3_arr, cop_arr, fab_arr, mrt_arr, nas_arr,srt_arr, tan_arr

# 计算中值矩阵
median_matrix = np.median(matrices, axis=0)

outpath = r"E:\Zhang_XinGang\17_LoessDEM\03_data\slo\slo.tif"
CreateGeoTiff(outpath, median_matrix, ast_Xsize, ast_Ysize, GeoT, Projection, 1000000)
