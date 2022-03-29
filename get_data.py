#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Script created on Tue Mar 29 11:49:35 2022
@author: Samantha Cruz
"""


import os

# More information
# https://www.data.jma.go.jp/mscweb/data/monitoring/gsics/ir/techinfo_mt1r.html


outdir = '/home/samanthalof/git/Satellite_Imagery_Analysis/data/'

os.sytem('w get --directory-prefix='+outdir+' https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/hsd_sampleB/NC_H08_20161117_0230_JP02.zip')

# we only need bands 3 (VIS - 1km), 7 (IR4), 8 (IR3), 13 (IR1), 15 (IR2),
# Removing bands we don't want 
os.sytem('rm NC_H08_20161117_0230_B02_JP02_R10.nc.bz2 NC_H08_20161117_0230_B04_JP02_R10.nc.bz2 NC_H08_20161117_0230_B05_JP02_R20.nc.bz2 NC_H08_20161117_0230_B06_JP02_R20.nc.bz2 NC_H08_20161117_0230_B09_JP02_R20.nc.bz2 NC_H08_20161117_0230_B10_JP02_R20.nc.bz2 NC_H08_20161117_0230_B11_JP02_R20.nc.bz2 NC_H08_20161117_0230_B12_JP02_R20.nc.bz2 NC_H08_20161117_0230_B14_JP02_R20.nc.bz2 NC_H08_20161117_0230_B16_JP02_R20.nc.bz2 NC_H08_20161117_0230_JP02.zip')

# unzip nc files
os.sytem('bunzip2 *bz2')

# Now we are ready to work !