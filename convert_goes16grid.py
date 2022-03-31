#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Script created on Wed Mar 30 18:29:55 2022
@author: Samantha Cruz
"""

import xarray as xr
import numpy as np

# open file with xarray
ds = xr.open_dataset('data/goes16/23-04/OR_ABI-L2-CMIPF-M3C10_G16_s20181131300445_e20181131311223_c20181131311296.nc')

# retrieving information we need to convert
x = ds.x.values # latitude in radians
y = ds.y.values # longitude in radians
lon_origin = ds.goes_imager_projection.longitude_of_projection_origin
H = ds.goes_imager_projection.perspective_point_height+ds.goes_imager_projection.semi_major_axis
r_eq = ds.goes_imager_projection.semi_major_axis
r_pol = ds.goes_imager_projection.semi_minor_axis

# create meshgrid filled with radian angles
x,y = np.meshgrid(x,y)

# lat/lon calc routine from satellite radian angle vectors
lambda_0 = (lon_origin*np.pi)/180.0

a = np.power(np.sin(x),2.0) + (np.power(np.cos(x),2.0)*(np.power(np.cos(y),2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(y),2.0))))
b = -2.0*H*np.cos(x)*np.cos(y)
c = (H**2.0)-(r_eq**2.0)

r = (-1.0*b - np.sqrt((b**2)-(4.0*a*c)))/(2.0*a)

s_x = r*np.cos(x)*np.cos(y)
s_y = - r*np.sin(x)
s_z = r*np.cos(x)*np.sin(y)

lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)

# verify calculated lat/lon is close enough to the nc attribute
print(np.nanmin(lat), ds.geospatial_lat_lon_extent.geospatial_southbound_latitude)
print(np.nanmax(lat), ds.geospatial_lat_lon_extent.geospatial_northbound_latitude)
print(np.nanmin(lon), ds.geospatial_lat_lon_extent.geospatial_westbound_longitude)
print(np.nanmax(lon), ds.geospatial_lat_lon_extent.geospatial_eastbound_longitude)

ds_latlon = xr.Dataset(
    data_vars=dict(
        Latitude=(["x", "y"], lat),
        Longitude=(["x", "y"], lon),
    ),
    attrs=dict(description="GOES 16 grid in lat/lon degrees format"),
)

ds_latlon.to_netcdf("data/goes16/goes16_latlon_grid.nc")
