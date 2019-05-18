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
    

#def promedio_cercanos(data,posicion,numero_vecinos):

#%%
carpeta='C:/Users/DG/Desktop/Laboratorio 6 Caprile Rosenberg/labo6-master/mediciones/5-8/-45/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-15/19.97/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)


#exitos=np.array([2,7,9])       
#for j in range(int(len(indice)/2)):
#for j in exitos:
j=2

bobina=Csv(carpeta,2*j,es_bobina=True)
resistencia=Csv(carpeta,2*j+1)
resistencia.filtrar_por_vecinos(10)
bobina.sacar_lineal()
pico_bobina=bobina.encontrar_picos(0.8,distancia_entre_picos=100,valle=True)
pico_resistencia=resistencia.encontrar_picos(0.8,distancia_entre_picos=100)
tiempo0=bobina.x[pico_bobina]
bobina.x-=tiempo0
altura_pico_bobina=bobina.y[pico_bobina]
resistencia.x-=tiempo0
#bobina.plot(fig_num=j,tamañox=14,tamañoy=8,color='r-')
resistencia.plot(fig_num=j,escala=-1/altura_pico_bobina,tamañox=14,tamañoy=6,color='b-')
#plt.plot(bobina.x[pico_bobina],bobina.y[pico_bobina],'g*')
#plt.plot(resistencia.x[pico_resistencia],resistencia.y[pico_resistencia],'g*')

posicion_x=np.where(abs(resistencia.x-3.2*10**-6)==min(abs(resistencia.x-3.2*10**-6)))

print(resistencia.y[posicion_x])

tensionesm45=np.array([-1.14,-0.93,-0.8,-0.94])








#%%
#indice=[]
#for archivo in os.listdir(carpeta):
#    if archivo.endswith(".csv"):
#        indice.append(archivo)

#nombre=indice[j]
#data = genfromtxt(carpeta+nombre, delimiter=',')
#
#data=data[1:,:]
#plt.figure(num=j, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
#
#plt.plot(data[:,0],data[:,1])
#




#b=pd.read_csv(carpeta+nombre,header=None)
#a=np.loadtxt(carpeta+nombre,delimiter=',')