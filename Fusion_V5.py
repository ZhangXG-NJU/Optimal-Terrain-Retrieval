# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import warnings
import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree
from geopandas import read_file as grf
from rasterio import open as rio

warnings.filterwarnings(action="ignore", category=FutureWarning)

def load_dem(names, paths):
    return {dem: (rio(path), rio(path).read(1)) for dem, path in zip(names, paths)}

def zero_like(ref_arr, dtype):
    return np.zeros_like(ref_arr, dtype=dtype)

def pixel_cent_coords(transform, x, y):
    return transform * (x + 0.5, y + 0.5)

def init_fus_params(dems):
    fus_trans = dems['ast'][0].transform
    fus_prof = dems['ast'][0].profile
    fus_arr = zero_like(dems['ast'][1], np.float32())
    msk_arr = zero_like(dems['ast'][1], np.uint8())
    return fus_trans, fus_prof, fus_arr, msk_arr

def weighted_mean(coords, near_pnts_id, pnts, err_cols):
    dists = np.linalg.norm(pnt_coords[near_pnts_id] - coords, axis=1)
    w = 1 / dists
    w /= np.sum(w)
    nearest_pnts_values = pnts.loc[near_pnts_id, err_cols].values
    return np.average(nearest_pnts_values, axis=0, weights=w)

def save_tiff(path, arr, prof):
    with rio(path, 'w', **prof) as destination:
        destination.write(arr, 1)

# Testing Define constants
# lidar_path = "../04_fustest/lidar.gpkg"
# dem_names = ['ast', 'aw3', 'cop', 'fab', 'nas', 'srt', 'tan']
# dem_paths = [f"../04_fustest/{dem}.tif" for dem in dem_names]
# fus_path = "../04_fustest/fus2.tif"
# msk_path = "../04_fustest/fus2_mask.tif"
# err_paths = [f"../04_fustest/{dem}_err2.tif" for dem in dem_names]

for part in range(1263, 1264):
    try:
        print(part)
        # True Define constants
        dem_names = ['ast', 'aw3', 'cop', 'fab', 'nas', 'srt', 't30']
        dem_paths = [f"../03_data/dem/03_crg_sub/{dem}_{part}.tif" for dem in dem_names]
        lidar_path = f"../03_data/lidars/03_sub/lidar_{part}.gpkg"
        fus_path = f"../03_data/fus/fusionv7/fus_{part}.tif"
        msk_path = f"../03_data/fus/fusionv7/fus_{part}_mask.tif"
        err_paths = [f"../03_data/fus/fusionv7/{dem}_err_{part}.tif" for dem in dem_names]
        
        # Load lidar data and preprocess
        pnts = grf(lidar_path)
        err_cols = [f"{dem}_err" for dem in dem_names]
        pnts[err_cols] = pnts[err_cols].abs()
        dems = load_dem(dem_names, dem_paths)
        
        # Precompute point coordinates and build KDTree
        pnt_coords = np.array(pnts.geometry.apply(lambda geom: (geom.x, geom.y)).tolist())
        tree = cKDTree(pnt_coords)
        radius = 1.1343344258429198
        max_pnts = 40
        
        # Initialize fusion parameters
        fus_trans, fus_prof, fus_arr, msk_arr = init_fus_params(dems)
        err_arrs = [zero_like(fus_arr, np.float32()) for _ in dem_names]
        
        # Process each pixel
        y_coords = np.arange(fus_arr.shape[0])
        x_coords = np.arange(fus_arr.shape[1])
        
        for y in tqdm(y_coords):
            for x in x_coords:
                dem_value = dems['ast'][1][y, x]
                if dem_value == 1000000:
                    fus_arr[y, x] = np.nan
                    msk_arr[y, x] = 0
                else:
                    coords = pixel_cent_coords(fus_trans, x, y)
                    pnts_in_r_id = tree.query_ball_point(coords, radius)
                    near_pnts_id = pnts_in_r_id if len(pnts_in_r_id) < max_pnts else tree.query(coords, k=max_pnts)[1]
                    weighted_mean_values = weighted_mean(coords, near_pnts_id, pnts, err_cols)
            
                    for i, dem in enumerate(dem_names):
                        err_arrs[i][y, x] = weighted_mean_values[i]
            
                    best_dem = dem_names[np.argmin(weighted_mean_values)]
                    best_dem_arr = dems[best_dem][1]
            
                    fus_arr[y, x] = best_dem_arr[y, x]
                    msk_arr[y, x] = dem_names.index(best_dem) + 1
        
        # Save the results
        save_tiff(fus_path, fus_arr, fus_prof)
        save_tiff(msk_path, msk_arr, fus_prof)
        for i, err_path in enumerate(err_paths):
            save_tiff(err_path, err_arrs[i], fus_prof)

    except Exception as e:
        print(f'{e}')
        continue

