# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:36:16 2020

@author: khoramian.a
"""
import rasterio
import rasterio.features
import rasterio.warp
import rasterio.mask

def maskingfiles(inputrasterpath,outrasterpath,maskpath='D:/PCP/data/maskfile.tif'):
    with rasterio.open(maskpath) as dataset:
    
        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()
    
        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):
    
            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                dataset.crs, 'EPSG:4326', geom, precision=6)
    
            # Print GeoJSON shapes to stdout.
            msk=[geom]
        
    
    src=rasterio.open(inputrasterpath)
    out_image, out_transform = rasterio.mask.mask(src, msk, crop=True)
    out_meta = src.meta
    
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    
    with rasterio.open(outrasterpath, "w", **out_meta) as dest:
        dest.write(out_image)
        


# import matplotlib.pyplot as plt
# import geopandas as gpd
# p = gpd.GeoSeries(msk)
# p.plot()
# plt.show()