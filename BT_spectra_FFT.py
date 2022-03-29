#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Script created on Tue Mar 29 18:26:57 2022
@author: Samantha Cruz
"""
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import make_interp_spline

# open file with xarray
ds = xr.open_dataset('data/NC_H08_20161117_0230_B13_JP02_R20.nc')

# Creating a array with the same resolution as lat lon
longitude = ds.longitude.values
latitude = ds.latitude.values
tb = ds.tbb.values

# found out that the resolution is 0.02, so creating a array with the same spacing
trans_long = np.arange(125, 145, 0.02)
trans_lat = np.arange(25, 45, 0.02)

# creating a list with tb values in the transect
trans_tb=[]
for i in range(1000):
    x = np.where(latitude == trans_lat[i])
    y = np.where(longitude == trans_long[i])
    trans_tb.append(ds.tbb.isel()[x[0][0],y[0][0]].values)
    
'''------------------------------------------------------------- '''
'''  CALCULATING BT SPECTRA USING FAST FOURIER TRANSFORMS (FFT)  '''
'''------------------------------------------------------------- '''

from scipy.fft import fft, ifft, rfft

# Compute the 1-D discrete Fourier Transform.
bt_spectra_fft = fft(trans_tb)
bt_spectra_fft[0]=0
# VISUALIZE
fig = plt.figure()
ax = plt.axes()
ax.plot(trans_long, bt_spectra_fft);
plt.title("Brightness Temperature spectra along the transect")
ax.grid(True, alpha=0.5)
ax.set_ylabel('Fourier transformed')
ax.set_xlabel('Longitude')
plt.savefig('FFT_bt_transect.png', dpi=320)

# Compute the 1-D inverse discrete Fourier Transform.
bt_spectra_ifft = ifft(trans_tb)
bt_spectra_ifft[0]=0
# VISUALIZE
fig = plt.figure()
ax = plt.axes()
ax.plot(trans_long, bt_spectra_ifft);
plt.title("Brightness Temperature spectra along the transect")
ax.grid(True, alpha=0.5)
ax.set_ylabel('inverse Fourier transformed')
ax.set_xlabel('Longitude')


# Compute the 1-D discrete Fourier Transform for real input.
bt_spectra_rfft = rfft(trans_tb)
bt_spectra_rfft[0]=0
# VISUALIZE
fig = plt.figure()
ax = plt.axes()
ax.plot(trans_long[0:501], bt_spectra_rfft);
plt.title("Brightness Temperature spectra along the transect")
ax.grid(True, alpha=0.5)
ax.set_ylabel('inverse Fourier transformed')
ax.set_xlabel('Longitude')

'''------------------------------------------------------------- '''
'''  Estimate power spectral density (PSD)    '''
'''------------------------------------------------------------- '''

from scipy import signal

# using a periodogram
f, Pxx_den = signal.periodogram(trans_tb, 0.02)
Pxx_den[0] = Pxx_den[1]
plt.semilogy(f, Pxx_den)
 # not sure this label is the right information in the axis
plt.xlabel('Wavenumber [m ⁻¹]')
plt.ylabel('PSD [K² m]')
plt.grid(alpha = 0.5)
plt.show()

# using Welch’s method
f, Pxx_den = signal.welch(trans_tb, 0.02)
Pxx_den[0] = Pxx_den[1]
plt.semilogy(f, Pxx_den)
 # not sure this label is the right information in the axis
plt.xlabel('Wavenumber [m ⁻¹]')
plt.ylabel('PSD [K² m]')

# Trying to plot a trend line, but failed:
# plt.grid(alpha = 0.5, ls=':', which='both')
# p = np.polyfit(np.log10(f), np.log10(Pxx_den), 1)
# trendline = np.poly1d(p)
# plt.plot(f, 10**trendline(f), "r--")
plt.show()

# implementing second-order polynomial detrending with Welch’s method
trans_tb_detrend = np.polyval(np.polyfit(trans_long, trans_tb, 3), trans_long)
f, Pxx_den = signal.welch(trans_tb_detrend, 0.02)
Pxx_den[0] = Pxx_den[1]
plt.semilogy(f, Pxx_den)
 # not sure this label is the right information in the axis
plt.xlabel('Wavenumber [m ⁻¹]')
plt.ylabel('PSD [K² m]')
plt.grid(alpha = 0.5, ls=':', which='both')
plt.show()

# Changed the plot type to plt.loglog (both axis in log)
f, Pxx_den = signal.welch(trans_tb, 0.02)
Pxx_den[0] = Pxx_den[1]
plt.loglog(f, Pxx_den,'-k')
 # not sure this label is the right information in the axis
plt.xlabel('Wavenumber [m ⁻¹]')
plt.ylabel('PSD [K² m]')
plt.grid(alpha = 0.5, ls=':', which='both')
plt.show()
plt.savefig('PSD_logscale.png', dpi=320)
