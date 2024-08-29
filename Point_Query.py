# -*- coding: utf-8 -*-
# author: Zhang_XinGang, NJU

import numpy             as     np
import geopandas         as     gpd
from   rasterstats       import point_query as pqr

lidarpth = r"D:\03_LPDEM\03_data\gedi\06_50val\gedi_11.gpkg"
lidar  = gpd.read_file(lidarpth)

ast    = r"..\03_data\dem\03_crg\dem_ast.tif"
aw3    = r"..\03_data\dem\03_crg\dem_aw3.tif"
cop    = r"..\03_data\dem\03_crg\dem_cop.tif"
fab    = r"..\03_data\dem\03_crg\dem_fab.tif"
nas    = r"..\03_data\dem\03_crg\dem_nas.tif"
srt    = r"..\03_data\dem\03_crg\dem_srt.tif"
t30    = r"..\03_data\dem\03_crg\dem_t30.tif"
fus    = r"D:\03_LPDEM\04_output\step1_fusion\fus.tif"

# pq_ast = np.round(np.array(pqr(lidar['geometry'], ast, interpolate='bilinear')),4)
# pq_aw3 = np.round(np.array(pqr(lidar['geometry'], aw3, interpolate='bilinear')),4)
# pq_cop = np.round(np.array(pqr(lidar['geometry'], cop, interpolate='bilinear')),4)
# pq_fab = np.round(np.array(pqr(lidar['geometry'], fab, interpolate='bilinear')),4)
# pq_nas = np.round(np.array(pqr(lidar['geometry'], nas, interpolate='bilinear')),4)
# pq_srt = np.round(np.array(pqr(lidar['geometry'], srt, interpolate='bilinear')),4)
# pq_t30 = np.round(np.array(pqr(lidar['geometry'], t30, interpolate='bilinear')),4)

pq_fus = np.round(np.array(pqr(lidar['geometry'], fus, interpolate='bilinear')),4)


np.savetxt("pq_fus_11.csv", pq_fus, delimiter=',', header='pq_fus', comments='', fmt='%.4f')

