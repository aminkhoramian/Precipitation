# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 11:04:33 2020

@author: khoramian.a
"""

from nasadap import Nasa, parse_nasa_catalog

###############################
### Parameters

username = 'aminkhoramian' # Need to change!
password = 'facb040be1e8' # Need to change!
mission = 'gpm'
product = '3IMERGHH'
version = 6
from_date = '2019-03-28'
to_date = '2019-03-29'
dataset_type = 'precipitationCal'
min_lat=-49
max_lat=-33
min_lon=165
max_lon=180
cache_dir = 'nasa/cache/nz'

###############################
### Examples

min_max1 = parse_nasa_catalog(mission, product, version, min_max=True) # Will give you the min and max available dates for products

ge1 = Nasa(username, password, mission, cache_dir)

products = ge1.get_products()

datasets = ge1.get_dataset_types(products[0])

ds1 = ge1.get_data(product, version, dataset_type, from_date, to_date, min_lat,
                    max_lat, min_lon, max_lon)
ge1.close()