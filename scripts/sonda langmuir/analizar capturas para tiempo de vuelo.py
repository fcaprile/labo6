# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:47:22 2019

@author: DG
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 13 00:05:48 2019

@author: ferchi
"""

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
from scipy.integrate import cumtrapz as integrar
#plt.clf()
#plt.close()

#carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-10/'




class Data:        
    def sacar_offset(self,n):
        suma=0
        for valor in self.y[:n]:
            suma+=valor
        suma/=n
        self.y=self.y-suma
    
    def filtrar_por_vecinos(self,n_vecinos=15):
        yfilt=[]
        for i in range(len(self.y)):
            if i>n_vecinos and i<len(self.y)-n_vecinos:
                suma=0
                for j in range(n_vecinos):
                    suma+=self.y[i+j]+self.y[i-j]
                yfilt.append(suma/(2*n_vecinos+1))
            if i<n_vecinos:
                suma=0
                for j in range(i):
                    suma+=self.y[i+j]+self.y[i-j]
                yfilt.append(suma/(2*i+1))
            if i>len(self.y)-n_vecinos:
                suma=0
                for j in range(len(self.y)-i):
                    suma+=self.y[i+j]+self.y[i-j]
                yfilt.append(suma/(2*(len(self.y)-i)+1))            
        yfilt.append(0)
        yfilt.append(0)
        self.y=np.array(yfilt)

    def calibrar_bobina(self,num_vecinos=20):
#        self.y=self.filtrar_por_vecinos(num_vecinos)
        self.y=integrar(self.y,self.x)
        A=9.72*10**8
        B=0.911
        self.y*=A
        self.x=self.x[1:]*B
        self.y*=-1
        self.x-=0.7*10**-6
        
    def encontrar_picos(self,porcentaje_altura,distancia_entre_picos=1,valle=False,plotear=False):
        if valle==False:            
            picos=detect_peaks(self.y,max(self.y)*porcentaje_altura,distancia_entre_picos,show=plotear)
        if valle==True:            
            picos=detect_peaks(self.y,min(self.y)*porcentaje_altura,distancia_entre_picos,valley=valle,show=plotear)
        return picos
    def sacar_lineal(self):
        recta=np.linspace(self.y[0],self.y[-1],len(self.y))
        self.y-=recta
   

     
class Csv(Data):
    def __init__ (self,carpeta,numero_de_archivo,es_bobina=False):
        nombre=indice[numero_de_archivo]        
        self.values=genfromtxt(carpeta+nombre, delimiter=',')
        self.values=self.values[1:,:]
        self.x=np.array(self.values[:,0])
        self.y=np.array(self.values[:,1])
        if es_bobina==True:
            super().sacar_offset(50)
            super().calibrar_bobina()
            
    def plot(self,fig_num=0,escala=1,tamañox=14,tamañoy=10,color='b-'):
        plt.figure(num= fig_num , figsize=(tamañox, tamañoy), dpi=80, facecolor='w', edgecolor='k')        
        plt.plot(self.x,self.y*escala,color)
        plt.grid(True) # Para que quede en hoja cuadriculada
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Tension (V)')

def plot(x,y,fig_num=0,escala=1,color='b-'):
    plt.figure(num= fig_num , figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')        
    plt.plot(x,y*escala,color)
    plt.grid(True) # Para que quede en hoja cuadriculada
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Tension (V)')
    
    
#%%
carpeta='C:/Users/DG/Desktop/Laboratorio 6 Caprile Rosenberg/labo6-master/mediciones/5-8/60/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/Mediciones filtradas (saque las feas)/5-11/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)


curvasresistencias=np.zeros([int(len(indice)/2)])
j=4
bobina=Csv(carpeta,2*j,es_bobina=True)
resistencia=Csv(carpeta,2*j+1)
#resistencia.y-=ruido
resistencia.filtrar_por_vecinos(20)
bobina.sacar_lineal()
pico_bobina=bobina.encontrar_picos(0.8,distancia_entre_picos=100,valle=True)
pico_resistencia=resistencia.encontrar_picos(0.8,distancia_entre_picos=100)
altura_pico_bobina=bobina.y[pico_bobina]
tiempo0=bobina.x[pico_bobina]
bobina.x-=tiempo0
resistencia.x-=tiempo0
bobina.plot(fig_num=1,tamañox=14,tamañoy=6,color='b-')
resistencia.plot(fig_num=1,escala=200,tamañox=14,tamañoy=10,color='r-')
plot(bobina.x[pico_bobina],bobina.y[pico_bobina],fig_num=1,color='g*')
plot(resistencia.x[pico_resistencia],resistencia.y[pico_resistencia]*200,fig_num=1,color='g*')
    
dt=np.array([3.36,3.24,3.4,2.97,2.99,3.26]) #mas o menos 3.19 entonces posicion 1917
print(np.mean(dt))
print(np.where(abs(resistencia.x)))