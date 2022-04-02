#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Script created on Thu Mar 31 11:16:28 2022
@author: Samantha Cruz
"""

import os
from ftplib import FTP

def grabFile(filename): # FTP download and save function
    # if the file already exists, skip it
    if os.path.isfile(local_dir+'/'+filename):
        return
    
    localfile = open(local_dir+'/'+filename, 'wb') # local download
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024) # FTP saver

    localfile.close() # close local file
    
ftp = FTP('ftp.avl.class.noaa.gov')  # connect to NOAA's FTP
ftp.login() # login anonymously
ftp.cwd('./8187450758/001') # navigate to exact FTP folder where data is located

files = ftp.nlst() # collect file names into vector

# Creates a local GOES repository in the current directory
local_dir = './data/goes16/23-04'
if os.path.isdir(local_dir)==False:
    os.mkdir(local_dir)

# loop through files and save them one-by-one
for filename in files:
    grabFile(filename)

ftp.quit() # close FTP connection