# -*- coding: utf-8 -*-
"""
Created on Sun May 19 23:59:31 2019

@author: ferchi
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz,filtfilt
from matplotlib import pyplot as plt
import os

carpeta='C:/Users/DG/Desktop/Laboratorio 6 Caprile Rosenberg/labo6-master/mediciones/5-15/27.77/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-15/64.4/'
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

def promediar_vectores(matriz): #formato: filas de vectores
    columnas=len(matriz[0,:])
    filas=len(matriz[:,0])
    prom=np.zeros(columnas)
    para_prom=np.zeros(filas,columnas)
    for j in range(columnas):
        prom[j]=np.mean(para_prom[:,j])

def posicion_x(x,valorx):
    posicion_x=np.where(abs(x-valorx)==min(abs(x-valorx)))[0][0]
    return posicion_x
    
#%%
carpeta_base='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-15/'
indice_carpetas=[]
for nombre in os.listdir(carpeta_base):
    indice_carpetas.append(nombre)


limites=np.array([[2.8,6],[2.8,5],[3.5,6],[3.5,5]])
for a,b in limites:
    corrientes=[]
    error_corrientes=[]
    for i in indice_carpetas:
        carpeta=carpeta_base+i+'/'
        indice=[]
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".csv"):
                indice.append(archivo)
        corrientes_matriz=[]
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
    #        y=filtrar(data)
            #promedio entre 3 y 5 us
            t1=a*10**-6
            t2=b*10**-6
            pos1=posicion_x(tiempo,t1)
            pos2=posicion_x(tiempo,t2)
            corrientes_matriz.append(np.mean(data[pos1:pos2]))
        corrientes.append(np.mean(corrientes_matriz))
        error_corrientes.append(np.std(corrientes_matriz)/np.sqrt(len(corrientes_matriz)))
        #    plt.figure(num= 0 , figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
            #plt.plot(tiempo, data, 'b-', label='data')
        #    plt.plot(bobina.x,bobina.y/1200)
    print('Carpeta',i,'analizada!')

    error_corrientes=np.array(error_corrientes)
    corrientes=np.array(corrientes)
    tensiones=[]
    for i in indice_carpetas:
        tensiones.append(float(i))
    tensiones=np.array(tensiones)
    
    
    #plt.figure(num= 0 , figsize=(16, 11), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(tensiones,corrientes,'b*')
    plt.errorbar(tensiones,corrientes,error_corrientes,linestyle = 'None')
    plt.ylabel('Corriente')
    plt.xlabel('Tensión (V)')
    plt.grid()

#np.savetxt('curva carac 8-5 entre 3,5 y 5 con error.txt',[tensiones,corrientes,error_corrientes], delimiter='\t')

#%% Comparacion curvas

tensiones8,corrientes8,error_corrientes8=np.loadtxt('curva carac 8-5 entre 3,5 y 5 con error.txt',delimiter='\t')
tensiones15,corrientes15,error_corrientes15=np.loadtxt('curva carac entre 3,5 y 5 con error.txt',delimiter='\t')

pos8=posicion_x(tensiones8,0)
pos15=posicion_x(tensiones15,0)
offset8=corrientes8[pos8]
offset15=corrientes15[pos15]

plt.plot(tensiones8,corrientes8-offset8,'b*',label='Mediciones del 8/5')
plt.errorbar(tensiones8,corrientes8-offset8,error_corrientes8,linestyle = 'None')
plt.plot(tensiones15,corrientes15/2-offset15/2,'g*',label='Mediciones del 15/5')
plt.errorbar(tensiones15,corrientes15/2-offset15/2,error_corrientes15/2,linestyle = 'None')
plt.ylabel('Corriente')
plt.xlabel('Tensión (V)')
plt.grid()

