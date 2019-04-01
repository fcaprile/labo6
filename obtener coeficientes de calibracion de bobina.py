# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 19:58:11 2019

@author: ferchi
"""

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
plt.clf()
plt.close()

#carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/Mediciones_25-03/posta/'
#carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        indice.append(archivo)
        
def filtrar_por_vecinos(y,n_vecinos):
    yfilt=[]
    for i in range(len(y)):
        if i>n_vecinos and i<len(y)-n_vecinos:
            suma=0
            for j in range(n_vecinos):
                suma+=y[i+j]+y[i-j]
            yfilt.append(suma/(2*n_vecinos+1))
        if i<n_vecinos:
            suma=0
            for j in range(i):
                suma+=y[i+j]+y[i-j]
            yfilt.append(suma/(2*i+1))
        if i>len(y)-n_vecinos:
            suma=0
            for j in range(len(y)-i):
                suma+=y[i+j]+y[i-j]
            yfilt.append(suma/(2*(len(y)-i)+1))            
    yfilt.append(0)
    yfilt.append(0)
    yfilt=np.array(yfilt)
    return(yfilt)
j=1
#kes=np.array([0,2,12,27,54,56,60,64,83,96])

n=75
nk=0
nombre=indice[j+int(len(indice)/2)]
dataR = np.loadtxt(carpeta+nombre, delimiter='\t')
medicionesR=np.zeros([len(dataR[:,0]),len(dataR[0,:])])
#cargo datos    
tR=dataR[0,:]
for i in range(len(dataR[:,0])-1):
    medicionesR[i,:]=dataR[i+1,:]
nombre=indice[j]
dataB = np.loadtxt(carpeta+nombre, delimiter='\t')
medicionesB=np.zeros([len(dataB[:,0]),len(dataB[0,:])])
t=dataB[0,:]
for i in range(len(dataB[:,0])-1):
    medicionesB[i,:]=dataB[i+1,:]
#un for para cada medicion
    
A=np.zeros(len(mediciones[0,:,0]))
for k in range(len(mediciones[0,:,0])):#k=0
    #resistencia
    R=0.55
    yR=medicionesR[k,:-100]/R
    yR=filtrar_por_vecinos(yR,n)
#
#    plt.plot(tR[:-100],yR)

    i1 = detect_peaks(yR, mph=min(yR)*0.75, mpd=600,show=False, valley=True)
    #bobina    
        
    yB=-medicionesB[k,:]
    yB=filtrar_por_vecinos(yB,n)
    
#    yoff=np.mean(y[0:50])
#    y-=yoff
    yint=integrar(yB,t)
#    yint=yB[1:]
    i2 = detect_peaks(yint, mph=min(yint)*0.75, mpd=100,show=False, valley=True)
    if len(i2)>0 and len(i1)>0:
        A[nk] = np.divide(yR[i1[0]], yint[i2[0]])
        tB=t-t[i2[0]]+t[i1[0]]
#        plt.figure(num=j+k, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
#        plt.plot(tB[:-1],yint*A[nk],'b')    
#        #plt.plot(t,yB*1000,'b')
#        plt.plot(tR[:-100],yR,'r')
#        plt.grid(True)
    nk+=1
    
coeficientes=[]
for i in range(len(A)):
    if A[i]!=A[i-1]:
        coeficiente.append(A)
plt.hist(coeficientes,10)
plt.plot(np.arange(0,len(mediciones[0,:,0]),1),coeficiente,'b*')

