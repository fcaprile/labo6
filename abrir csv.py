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
#plt.clf()
#plt.close()

carpeta='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/4-10/'
#carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/27-03/'
indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):
        indice.append(archivo)

class Csv:
    def __init__ (self,carpeta,numero_de_archivo):
        nombre=indice[numero_de_archivo]        
        self.values=genfromtxt(carpeta+nombre, delimiter=',')
        self.values=self.values[1:,:]
        self.x=self.values[:,0]
        self.y=self.values[:,1]

    def plot(self,fig_num=0,escala=1,color='b-'):
        plt.figure(num= fig_num , figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')        
        plt.plot(self.x,self.y*escala,color)
    
        
for j in range(int(len(indice)/2)):
    data1=Csv(carpeta,j+1)
    data2=Csv(carpeta,j)
    data1.plot(fig_num=j,color='r-')
    data2.plot(fig_num=j,escala=10,color='b-')




















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