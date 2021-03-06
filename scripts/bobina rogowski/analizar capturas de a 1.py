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

#carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-3/'
#carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/'
#indice=[]
#for archivo in os.listdir(carpeta):
#    if archivo.endswith(".txt"):
#        indice.append(archivo)
        
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

def integrar_entre(y,x,ti,tf):
    i=int(np.where(abs(x-ti)==min(abs(x-ti)))[0])
    f=int(np.where(abs(x-tf)==min(abs(x-tf)))[0])
    yint_aux=integrar(y[i:f],x[i:f])
    zeros1=np.zeros(i)
    zeros2=np.zeros(len(y)-f)
    yint=np.concatenate((zeros1,yint_aux,zeros2), axis = 0)
    return yint

def calibrar(t,y):
    A=9.72*10**8
    B=0.911
    y*=A
    t*=B
    return y,t
#numero de archivo
j=0
#kes=np.array([0,2,12,27,54,56,60,64,83,96])#dia 4-1
#kes=np.array([8,9,22,30,37])#dia 4-3

n=5
nk=0
k=3

#leo los datos de la res
#nombre=indice[j+int(len(indice)/2)]
nombre='datoscanal2_punta100-2019-4-1-11-20.txt'
dataR = np.loadtxt(nombre, delimiter='\t')
medicionesR=np.zeros([len(dataR[:,0]),len(dataR[0,:])])
tR=dataR[0,:]
for i in range(len(dataR[:,0])-1):
    medicionesR[i,:]=dataR[i+1,:]

#leo los datos de la bobina
#nombre=indice[j]
nombre='datoscanal1_punta100-2019-4-1-11-20.txt'
dataB = np.loadtxt(nombre, delimiter='\t')
medicionesB=np.zeros([len(dataB[:,0]),len(dataB[0,:])])
t=dataB[0,:]
for i in range(len(dataB[:,0])-1):
    medicionesB[i,:]=dataB[i+1,:]
    
#resistencia
#ATENCION: chequear valor de R y signo de yR antes de correr el script
#R=0.55
yR=medicionesR[k,:-100]/R
#yR=filtrar_por_vecinos(yR,n)

plt.rcParams['font.size']=20#tamaño de fuente
plt.figure(num=0, figsize=(9,6), dpi=80, facecolor='w', edgecolor='k')
plt.subplots_adjust(left=0.14, bottom=0.13, right=0.98, top=0.98, wspace=None, hspace=None)

plt.plot(tR[:-100]*1000,yR,label='Resistencia')

i1 = detect_peaks(yR, mph=min(yR)*0.75, mpd=600,show=False, valley=True)
#bobina    
    
yB=-medicionesB[k,:]
yB=filtrar_por_vecinos(yB,n)
#plt.plot(t[:-100]*1000,yB[:-100]*1000,label='Bobina (mV)')
plt.xlabel('tiempo(ms)')
#plt.ylabel('Tensión')
plt.ylabel('Corriente(A)')

yoff=np.mean(yB[0:50])
yB-=yoff
yint=integrar(yB,t)
#yint=yR[1:]
i2 = detect_peaks(yint, mph=min(yint)*0.75, mpd=100,show=False, valley=True)
A = np.divide(yR[i1[0]], yint[i2[0]])
#A=9.72*10**8
#tR=t-t[i2[0]]+t[i1[0]]
#tR=(tR)*0.911+(-t[i2[0]]+t[i1[0]])*0.911
plt.plot(tR[:-1]*1000,yint*A,label='Bobina')
plt.legend(loc = 'best') 

#if len(i2)>0 and len(i1)>0:
#    A = np.divide(yR[i1[0]], yint[i2[0]])
#    tB=t-t[i2[0]]+t[i1[0]]
#    tB=(tB)*0.911+(-t[i2[0]]+t[i1[0]])*0.911
#    plt.plot(tB[:-1],yint*A,'b',label='Bobina')    
#    #plt.plot(t,yB*1000,'b')
#    plt.plot(tR[:-100],yR,'r',label='Resistencia')
#    plt.legend(loc='best')
#    plt.grid(True)
#    
#print('Archivo: ',indice[j])    
#print('El coeficiente fue:',A)




'''
plt.rcParams['font.size']=16#tamaño de fuente
plt.plot(np.array([1]),'r',label='0V')
plt.plot(1,1,'g',label='20V')
plt.plot(1,1,'y',label='40V')
plt.legend(loc = 'best') 
'''





















