# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 10:52:31 2019

@author: Admin
"""

from scipy import misc
import os

carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-10/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".wfm"):
        indice.append(archivo)


path = 'carpeta+'
image= misc.imread(os.path.join(path,'image.bmp'), flatten= 0)
