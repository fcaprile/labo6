# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 13:40:59 2019

@author: Admin
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/Mediciones_27-03'
carpeta='C:/Users/Admin/Desktop/Github labo 6/labo 6/mediciones/27-03/'

indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        indice.append(archivo)

nombre1=indice[2]
nombre2=indice[5]
data1 = pd.read_csv(carpeta+nombre1, delimiter='\t',header = None)
data2 = pd.read_csv(carpeta+nombre2, delimiter='\t',header = None)
        
data1=np.array(data1)
data2=np.array(data2)
mediciones=np.zeros([len(data1[:,0]),len(data1[0,:])-1])

tR=data2[:,0]
for i in range(len(data2[0,:])-1):
    mediciones[:,i]=data2[:,i+1]
    
yR=mediciones[:-100,0]
#    yR=filtrar_por_vecinos(yR,10)
#    plt.plot(tR[:-100],yR)
#    i1 = detect_peaks(yR, mph=-300, mpd=600, valley=True)
#hacer filtro para encontrar mejor el pico

#    nombre=indice[j]
#    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
#    data=np.array(data)
#    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
plt.grid(True)
t=data1[:,0]
for i in range(len(data1[0,:])-1):
    mediciones[:,i]=data1[:,i+1]
    
y=mediciones[:,0]

yoff=np.mean(y[0:50])
#    y-=yoff
#    yint=integrar(y,t)
#    i2 = detect_peaks(yint, mph=-0.00075, mpd=100, valley=True)
#    A = np.divide(yR[i1], yint[i2[0]])
#    tB=t-t[i2]+t[i1]
plt.plot(t,y*280/0.0003)    
plt.plot(tR[:-100],yR)
