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
ds = xr.open_dataset('data/goes16/OR_ABI-L2-CMIPF-M3C10.nc')

# retrieving information we need to convert
lat = ds.y.values # latitude in radians
lon = ds.x.values # longitude in radians
lon_origin = ds.goes_imager_projection.longitude_of_projection_origin
H = ds.goes_imager_projection.perspective_point_height+ds.goes_imager_projection.semi_major_axis
r_eq = ds.goes_imager_projection.semi_major_axis
r_pol = ds.goes_imager_projection.semi_minor_axis

# create meshgrid filled with radian angles
lat_rad,lon_rad = np.meshgrid(lat,lon)

# lat/lon calc routine from satellite radian angle vectors
lambda_0 = (lon_origin*np.pi)/180.0

a_var = np.power(np.sin(lat_rad),2.0) + (np.power(np.cos(lat_rad),2.0)*(np.power(np.cos(lon_rad),2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(lon_rad),2.0))))
b_var = -2.0*H*np.cos(lat_rad)*np.cos(lon_rad)
c_var = (H**2.0)-(r_eq**2.0)

r_s = (-1.0*b_var - np.sqrt((b_var**2)-(4.0*a_var*c_var)))/(2.0*a_var)

s_x = r_s*np.cos(lat_rad)*np.cos(lon_rad)
s_y = - r_s*np.sin(lat_rad)
s_z = r_s*np.cos(lat_rad)*np.sin(lon_rad)

lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)

# print test coordinates
print('{} N, {} W'.format(lat[318,1849],abs(lon[318,1849])))

# saving files to directory
np.savetxt('data/goes16/goes_lat.npy', lat)
np.savetxt('data/goes16/goes_lon.npy', lon)

# to open use lat = np.genfromtxt('data/goes16/goes_lat.npy')