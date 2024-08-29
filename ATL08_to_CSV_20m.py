# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import pandas as pd
import h5py
import os
import numpy as np

def read_icesat(fname):
    groups = ['/gt1l', '/gt2l', '/gt3l', '/gt1r', '/gt2r', '/gt3r']
    all_results = pd.DataFrame()

    for g in groups:
        try:
            result = pd.DataFrame()
            with h5py.File(fname, 'r') as fi:
                # Extract and flatten data

                result['lon']        = fi[g + '/land_segments/longitude_20m'][:].flatten()
                result['lat']        = fi[g + '/land_segments/latitude_20m'][:].flatten()
                result['lidar']      = fi[g + '/land_segments/terrain/h_te_best_fit_20m'][:].flatten()
                length = len(result['lon'])
                
                result['group']      = np.repeat(g, length)
                result['time']       = np.repeat(fi[g + '/land_segments/delta_time'][:], 5)[:length]
                result['lidar_ucrt'] = np.repeat(fi[g + '/land_segments/terrain/h_te_uncertainty'][:], 5)[:length]
                result['cnpy']       = np.repeat(fi[g + '/land_segments/canopy/h_canopy'][:], 5)[:length]
                result['cnpy_ucrt']  = np.repeat(fi[g + '/land_segments/canopy/h_canopy_uncertainty'][:], 5)[:length]
                result['te_flg']     = np.repeat(fi[g + '/land_segments/terrain_flg'][:], 5)[:length]
                result['ntephotons'] = np.repeat(fi[g + '/land_segments/terrain/n_te_photons'][:], 5)[:length]
                result['h_te_best']  = np.repeat(fi[g + '/land_segments/terrain/h_te_best_fit'][:], 5)[:length]
                result['cloud']      = np.repeat(fi[g + '/land_segments/cloud_flag_atm'][:], 5)[:length]
                result['night_flag'] = np.repeat(fi[g + '/land_segments/night_flag'][:], 5)[:length]
                
            # Filter the data
            dropindex = np.where((result['lidar']       > 9000) |
                                 (result['lidar']       < -422) |
                                 (result['lidar_ucrt']  > 7.5)  |
                                 (result['cloud'] > 1)          |
                                 (result['ntephotons']  <50)    |
                                 (result['night_flag'] == 1)    )  
            dropindex = np.array(dropindex).flatten()
            result = result.drop(index=list(dropindex))
            
            if result.empty: 
                print("File has no valuable Photons")
            else:
                ofilecsv = fname.replace('.h5', '_' + g[1:] + '.csv')
                print('out ->', ofilecsv)
                result.to_csv(ofilecsv, index=None)
                
        except Exception as e: 
            print(f'Failed for group {g}: {e}')
            continue

def readMultiH5(dir):
    for root_dir, sub_dir, files in os.walk(dir):
        for file in files:
            if file.endswith('h5'):
                # Absolute path
                file_name = os.path.join(root_dir, file)
                read_icesat(file_name)

readMultiH5(r"E:\Zhang_XinGang\17_LPDEM\03_data\atl08\01_raw\20231")
