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
        



for j in range(1):#int(len(indice)/2)
    plt.figure(num=j, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    nombre=indice[j]
    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
    data=np.array(data)
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
    plt.grid(True)
    t=data[:,0]
    for i in range(len(data[0,:])-1):
        mediciones[:,i]=data[:,i+1]
        
    y=mediciones[:,0]
    
    yint=integrar(y,x)
    
    
    plt.plot(t,yint)    
        
        
    nombre=indice[j+4]
    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
        
    data=np.array(data)
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
    
    t=data[:,0]
    for i in range(len(data[0,:])-1):
        mediciones[:,i]=data[:,i+1]
        
    y=mediciones[:,0]
    plt.plot(t,y)    
    

#inte=0
#for i in range(len(y)):
#    inte+=y[i]































