# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:10:25 2019
@author: Admin
"""
import pandas as pd
import math as m
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from array import array
import os
import sys
from scipy.integrate import cumtrapz as integrar
from scipy.signal import filtfilt as filtro 

carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/Mediciones_25-03/posta/'

indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        indice.append(archivo)
        

def filtrar_por_vecinos(y,n_vecinos):
    yfilt=[]
    for i in range(len(y)):
        if i>n_vecinos and i<len(y)-n_vecinos:
            yfilt.append((y[i]+y[i-n_vecinos]+y[i+n_vecinos])/3)
        if i<n_vecinos:
            yfilt.append((y[i]+y[i+n_vecinos])/2)
        if i>len(y)-n_vecinos:
            yfilt.append((y[i]+y[i-n_vecinos])/2)
            
    yfilt.append(0)
    yfilt.append(0)
    yfilt=np.array(yfilt)
    return(yfilt)

for j in range(1):#int(len(indice)/2)
    plt.figure(num=j, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
        
        
    nombre=indice[j+4]
    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
        
    data=np.array(data)
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
    
    tR=data[:,0]
    for i in range(len(data[0,:])-1):
        mediciones[:,i]=data[:,i+1]
        
    yR=mediciones[:-100,0]
#    yR=filtrar_por_vecinos(yR,10)
#    plt.plot(tR[:-100],yR)
    i1 = detect_peaks(yR, mph=-300, mpd=600, valley=True)
#hacer filtro para encontrar mejor el pico
    
    nombre=indice[j]
    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
    data=np.array(data)
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
    plt.grid(True)
    t=data[:,0]
    for i in range(len(data[0,:])-1):
        mediciones[:,i]=data[:,i+1]
        
    y=mediciones[:,0]
    
    yoff=np.mean(y[0:50])
    y-=yoff
    yint=integrar(y,t)
    i2 = detect_peaks(yint, mph=-0.00075, mpd=100, valley=True)
    A = np.divide(yR[i1], yint[i2[0]])
    tB=t-t[i2]+t[i1]
    plt.plot(tB,y)    
    plt.plot(tR[:-100],yR)


#inte=0
#for i in range(len(y)):
#    inte+=y[i]






























