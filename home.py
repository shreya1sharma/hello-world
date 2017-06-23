# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 18:41:00 2017

@author: hoge
"""
import os
import gdal
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import skimage
from skimage.filters import threshold_otsu
from skimage.filters import try_all_threshold
import cv2
import math
from skimage import img_as_ubyte
from skimage.morphology import convex_hull_image
import pandas as pd

file=
(fileRoot, fileExt)= os.path.splitext(file)

ds = gdal.Open(file)
band = ds.GetRasterBand(1)
arr = band.ReadAsArray()

[cols, rows] = arr.shape
#Applying Otsu Thresholding
thresh = threshold_otsu(arr)
binary = arr > thresh
points = binary>0
x_v1,y_v1= principal_component(points)

def principal_component(points):
    x,y = np.nonzero(points) #check x, y ??????
    x = x - np.mean(x)
    y = y - np.mean(y)
    coords = np.vstack([x, y])
    cov = np.cov(coords)
    evals, evecs = np.linalg.eig(cov)
    sort_indices = np.argsort(evals)[::-1]
    evec1, evec2 = evecs[:, sort_indices]
    x_v1, y_v1 = evec1  # Eigenvector with largest eigenvalue
    x_v2, y_v2 = evec2
    scale = 40
    plt.plot([x_v1*-scale*2, x_v1*scale*2],
         [y_v1*-scale*2, y_v1*scale*2], color='red')
    plt.plot([x_v2*-scale, x_v2*scale],
         [y_v2*-scale, y_v2*scale], color='blue')
    plt.plot(x,y, 'k.')
    plt.axis('equal')
    plt.gca().invert_yaxis()  # Match the image system with origin at top left
    plt.show()
    return x_v1, y_v1