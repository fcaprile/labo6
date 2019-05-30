# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:06:30 2019

@author: DG
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz,filtfilt
from matplotlib import pyplot as plt
import os

indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)
        

def filtrar(data):
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
    
    
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
    #    y = lfilter(b, a, data)
        y = filtfilt(b, a, data)
        return y
    
    
    # Filter requirements.
    order = 5
    fs = len(data)/(tiempo[-1]-tiempo[0])       # sample rate, Hz
    fs=1/(tiempo[1]-tiempo[0])
    cutoff =7*10**4  # desired cutoff frequency of the filter, Hz
    cutoff=4*10**5
    b, a = butter_lowpass(cutoff, fs, order)
    
    y = butter_lowpass_filter(data, cutoff, fs, order)
    return(y)


#%%        
carpeta='C:/Users/DG/Desktop/Laboratorio 6 Caprile Rosenberg/labo6-master/mediciones/5-15/27.77/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-15/52/'
j=2
R=Csv(carpeta,2*j+1)
bobina=Csv(carpeta,2*j,es_bobina=True)
bobina.sacar_lineal()
pico_bobina=bobina.encontrar_picos(0.8,distancia_entre_picos=100,valle=True)[0]
tiempo0=bobina.x[pico_bobina]
altura_pico_bobina=bobina.y[pico_bobina]
bobina.x-=tiempo0
R.x-=tiempo0
data=-R.y/altura_pico_bobina
tiempo=R.x
y=filtrar(data)



plt.figure(num= 0 , figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
plt.plot(tiempo, data, 'b-', label='data')
plt.plot( tiempo,y, 'g-', linewidth=2, label='filtered data')
#plt.plot(bobina.x,bobina.y/1200)
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()



#%%
def promediar(matriz): #formato: filas de vectores
    columnas=len(matriz[0,:])
    filas=len(matriz[:,0])
    prom=np.zeros(columnas)
    for j in range(columnas):
        prom[j]=np.mean(matriz[:,j])
    return prom

carpeta='C:/Users/DG/Desktop/Laboratorio 6 Caprile Rosenberg/labo6-master/mediciones/5-15/27.77/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-15/52/'

indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)
M=np.zeros([int(len(indice)/2),4000])
for j in range(int(len(indice)/2)):   
    R=Csv(carpeta,2*j+1)
    bobina=Csv(carpeta,2*j,es_bobina=True)
    bobina.sacar_lineal()
    pico_bobina=bobina.encontrar_picos(0.8,distancia_entre_picos=100,valle=True)[0]
    tiempo0=bobina.x[pico_bobina]
    altura_pico_bobina=bobina.y[pico_bobina]
    bobina.x-=tiempo0
    R.x-=tiempo0
    data=-R.y/altura_pico_bobina
    tiempo=R.x
#    y=filtrar(data)
    y=data
    M[j,:]=data
    plt.figure(num= 0 , figsize=(16, 11), dpi=80, facecolor='w', edgecolor='k')
    plt.plot( tiempo,y, 'g-', linewidth=2, label='filtered data')
promedio=promediar(M)
#plt.plot(tiempo,promedio)

#-64: entre 3.4 y 6
#-40: entre 3.2 y 5.6
#-20 2.4 5.3
#64  3 5.2
#45  3 4.8
#30  chan
#quedo entre 3 y 5
