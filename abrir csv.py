# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:35:12 2019

@author: Admin
"""
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
from numpy import genfromtxt
plt.clf()
plt.close()

carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-8/'
#carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)

j=0
nombre=indice[j]
data = genfromtxt(carpeta+nombre, delimiter=',')

data=data[1:,:]
plt.plot(data[:,0],data[:,1])
#b=pd.read_csv(carpeta+nombre,header=None)
#a=np.loadtxt(carpeta+nombre,delimiter=',')