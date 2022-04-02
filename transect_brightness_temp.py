#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Script created on Tue Mar 29 14:45:34 2022
@author: Samantha Cruz
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Lets start with BAND-13
inputfile = 'data/NC_H08_20161117_0230_B13_JP02_R20.nc'

# open file with xarray
ds = xr.open_dataset(inputfile)

# Visualize the brightness temperature
ds.tbb.isel().plot(x="longitude")

# plot a transect from the image
x_values = [125, 145]
y_values = [25, 45]
plt.plot(x_values, y_values, linewidth = 1, linestyle = "--", color = "black")

# plot all together
ds.tbb.isel().plot(x="longitude")
plt.plot(x_values, y_values, linewidth = 1, linestyle = "--", color = "black")

# Saving image
plt.savefig('figs/transect.png', dpi=320)

''' INTERPOLATING THE 2D BRIGHTNESS TEMP TO 1D TRANSECT '''

# Cortar a imagem para que não tenha nans
tbb_clean = ds

# Creating a array with the same resolution as lat lon
longitude = ds.longitude.values
latitude = ds.latitude.values
tb = ds.tbb.values

# Checking the resolution on both direction
np.diff(longitude).mean()
np.diff(latitude).mean()

# found out that the resolution is 0.02, so creating a array with the same spacing
trans_long = np.arange(x_values[0], x_values[1], 0.02)
trans_lat = np.arange(y_values[0], y_values[1], 0.02)

# creating a list with tb values in the transect
trans_tb=[]
for i in range(1000):
    x = np.where(latitude == trans_lat[i])
    y = np.where(longitude == trans_long[i])
    trans_tb.append(ds.tbb.isel()[x[0][0],y[0][0]].values)

# VISUALIZE
fig = plt.figure()
ax = plt.axes()
ax.plot(trans_long, trans_tb);
plt.title("Brightness Temperature along the transect")
ax.grid(True, alpha=0.5)
ax.set_ylabel('Brightness Temperature (K)')
ax.set_xlabel('Longitude')

plt.savefig('bt_along_transect.png', dpi=320)



