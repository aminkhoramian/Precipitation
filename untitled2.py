# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:50:01 2020

@author: khoramian.a
"""

import fiona
import rasterio
import rasterio.mask

with fiona.open("D:/Documents/Thesis/Thesis/2/Data/GIS/iran-ostan/OSTAN40_G.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
    
with rasterio.open("D:/PCP/ftp/202011/gpm_30mn_20201129_095959.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("RGB.byte.masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)