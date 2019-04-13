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

carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-10/'
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/4-10/20V/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)




class Data:
    def calibrar_bobina(self,num_vecinos=20):
#        self.y=filtrar_por_vecinos(self.y,num_vecinos)
        self.y=integrar(self.y,self.x)
        A=9.72*10**8
        B=0.911
        self.y*=A
        self.x=self.x[1:]*B
     
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
        self.y=yfilt


        
class Csv(Data):
    def __init__ (self,carpeta,numero_de_archivo,es_bobina=False):
        nombre=indice[numero_de_archivo]        
        self.values=genfromtxt(carpeta+nombre, delimiter=',')
        self.values=self.values[1:,:]
        self.x=self.values[:,0]
        self.y=self.values[:,1]
        if es_bobina==True:
            super().sacar_offset(50)
            super().calibrar_bobina(10)
            
    def plot(self,fig_num=0,escala=1,color='b-'):
        plt.figure(num= fig_num , figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')        
        plt.plot(self.x,self.y*escala,color)


def plot(x,y,fig_num=0,escala=1,color='b-'):
    plt.figure(num= fig_num , figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')        
    plt.plot(x,y*escala,color)
    
#%%
exitos=np.array([2,7,9])       
#for j in range(int(len(indice)/2)):
for j in exitos:
    data1=Csv(carpeta,j+1)
    data2=Csv(carpeta,j,es_bobina=True)
    data1.filtrar_por_vecinos(20)
    data1.plot(fig_num=j,color='r-')
    data2.plot(fig_num=j,escala=0.003,color='b-')



















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