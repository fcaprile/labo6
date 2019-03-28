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
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/'
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

for j in range(int(len(indice)/2)):
    nombre=indice[j+int(len(indice)/2)]
    data = np.loadtxt(carpeta+nombre, delimiter='\t')
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])])
    
    tR=data[0,:]
    for i in range(len(data[:,0])-1):
        mediciones[i,:]=data[i+1,:]
    for k in range(len(mediciones[:,0])):#k=0   
        yR=mediciones[k,:-100]
        yR=filtrar_por_vecinos(yR,1)
    #    plt.figure(num=j+k, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    #
    #    plt.plot(tR[:-100],yR)

        i1 = detect_peaks(yR, mph=min(yR)*0.75, mpd=600,show=False, valley=True)
    #hacer filtro para encontrar mejor el pico
        
        nombre=indice[j]
        data = np.loadtxt(carpeta+nombre, delimiter='\t')
        mediciones=np.zeros([len(data[:,0]),len(data[0,:])])
        t=data[0,:]
        for i in range(len(data[:,0])-1):
            mediciones[i,:]=data[i+1,:]
            
        yB=mediciones[k,:]
        
    #    yoff=np.mean(y[0:50])
    #    y-=yoff
        yint=integrar(yB,t)
        i2 = detect_peaks(yint, mph=max(yint)*0.75, mpd=100,show=False, valley=False)
        if len(i2)==1 and len(i1)==1:
            A = np.divide(yR[i1], yint[i2])
            tB=t-t[i2]+t[i1]
            plt.plot(tB[:-1],yint*A,'b')    
            #plt.plot(t,yB*1000,'b')
            plt.plot(tR[:-100],yR,'r')
            plt.grid(True)
            carpeta_guardar='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/graficos analisis/'
            plt.savefig(carpeta_guardar+nombre +'medición Nº'+ str(k)+'.png')
            plt.clf()
            plt.close()
        else:
            print('En la medición Nº '+str(k)+' no se pudo encontrar el pico correctamente')
#            plt.plot(t[:-1],-yint*100000000,'b')
#            plt.plot(tR[:-100],yR,'r')
            






























