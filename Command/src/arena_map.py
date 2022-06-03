# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys       

sys.path.append('D:/Command/Back-end2.0/')       

# sys.path.insert(1, 'D:/Command/Back-end2.0')       

# import coordinates


df = pd.read_csv('coordinates.txt')


# df.head()


# BBox = ((df.longitude.min(),   df.longitude.max(),      
#          df.latitude.min(), df.latitude.max())



# ruh_m = plt.imread('C:/.. … /Riyadh_map.png')



# fig, ax = plt.subplots(figsize = (8,7))
# ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.2, c='b', s=10)
# ax.set_title('Plotting Spatial Data on Riyadh Map')
# ax.set_xlim(BBox[0],BBox[1])
# ax.set_ylim(BBox[2],BBox[3])
# ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')