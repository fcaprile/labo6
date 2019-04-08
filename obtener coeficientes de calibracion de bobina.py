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
from scipy.signal import peak_widths as ancho 
from scipy.signal import find_peaks

plt.clf()
plt.close()

#carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/Mediciones_25-03/posta/'
#carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/4-1/'
carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/python/mediciones/4-3/'

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
j=0

#cargo datos    

nombre=indice[j+int(len(indice)/2)]
dataR = np.loadtxt(carpeta+nombre, delimiter='\t')
medicionesR=np.zeros([len(dataR[:,0]),len(dataR[0,:])])
tR=dataR[0,:]
for i in range(len(dataR[:,0])-1):
    medicionesR[i,:]=dataR[i+1,:]
nombre=indice[j]
dataB = np.loadtxt(carpeta+nombre, delimiter='\t')
medicionesB=np.zeros([len(dataB[:,0]),len(dataB[0,:])])
t=dataB[0,:]
for i in range(len(dataB[:,0])-1):
    medicionesB[i,:]=dataB[i+1,:]

def punto_cercano_al_valor(x,y,valor_y,i):
    pos=int(np.where((abs(y-valor_y))==min(abs(y-valor_y)))[i])
    return x[pos],y[pos]

#def ancho(x,y,valor_y):#solo funciona con funciones unimodales
#    pos1=int(np.where((abs(y-valor_y))==min(abs(y-valor_y)))[0])
#    pos2=int(np.where((abs(y-valor_y))==min(abs(y-valor_y)))[1])
#    return x[pos2]-x[pos1]
#

#%%
#ATENCION!!!!!!!: chequear valor de R y signo de yR antes de correr el script
    
#un for para cada medicion
n=50
#kes=np.array([0,2,12,27,54,56,60,64,83,96])
#kes=np.array([8,9,22,30,37])#dia 4-3  
A=np.zeros(len(medicionesR[:,0]))#coeficiente de amplitudes
#A=np.zeros(len(kes))#coeficiente de amplitudes
B=np.zeros(len(medicionesR[:,0]))#coeficientes de "ensanchado"
C=np.zeros(len(medicionesR[:,0]))#diferencia de tiempo
nk=0
for k in range(len(medicionesR[:,0])-1):
    #resistencia
    R=0.55
    yR=medicionesR[k,:-100]/R
    yR=filtrar_por_vecinos(yR,n)
#    plt.plot(tR[:-100],yR)

    iR, _   = find_peaks(-yR,-min(yR)*0.75,distance=100)#detect_peaks(yR, mph=min(yR)*0.75, mpd=600,show=False, valley=True)

    #bobina            
    yB=-medicionesB[k,:]
    yB=filtrar_por_vecinos(yB,n)
    
#    yoff=np.mean(y[0:50])
    yint=integrar(yB,t)
#    yint=yB[1:]
    iB, _  = find_peaks(-yint,-min(yint)*0.75,distance=100)#detect_peaks(yint, mph=min(yint)*0.75, mpd=100,show=False, valley=True)
    if len(iR)>0 and len(iB)>0:
        dt=t[1]-t[0]
        peaksR, _ = find_peaks(-yR,200,distance=100)
        A[nk] = np.divide(yR[iR[0]], yint[iB[0]])
        C[nk]=t[iR[0]]-t[iB[0]]
        anchoR_pos =ancho(-yR,iR,rel_height=1/np.sqrt(2))
        anchoR=t[int(anchoR_pos[3])]-t[int(anchoR_pos[2])]
        anchoB_pos =ancho(-yint,iB,rel_height=1/np.sqrt(2))
        anchoB=t[int(anchoB_pos[3])]-t[int(anchoB_pos[2])]
        B[nk]=np.divide(anchoR,anchoB)
        nk+=1
#        plt.figure(num=j+k, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
#        plt.plot(tB[:-1],yint*A[nk],'b')    
#        #plt.plot(t,yB*1000,'b')
#        plt.plot(tR[:-100],yR,'r')
#        plt.grid(True)
    if k%50==0 and k!=0:
        print('Ya se analizaron',k,'mediciones!')

if A[-1]==0:
    A=np.delete(A,-1)

if B[-1]==0:
    B=np.delete(B,-1)

if C[-1]==0:
    C=np.delete(C,-1)


#coeficiente ancho

coeficientes_ancho=[]
for i in range(len(B)):
    if B[i]!=B[i-1]:
        coeficientes_ancho.append(B[i])
coeficientes_ancho=np.array(coeficientes_ancho)
plt.figure(num=3, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
n,bins,patches=plt.hist(coeficientes_ancho,20,edgecolor='blue')
plt.title('Histograma de valores de la constante de ancho')
plt.xlabel('Valor de "B"')
plt.ylabel('Cantidad')

#coeficiente tiempo


coeficientes_tiempo=[]
for i in range(len(C)):
    if C[i]!=C[i-1]:
        coeficientes_tiempo.append(B[i])
coeficientes_tiempo=np.array(coeficientes_tiempo)
plt.figure(num=3, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
n,bins,patches=plt.hist(coeficientes_tiempo,20,edgecolor='blue')
plt.title('Histograma de valores de la diferencia temporal')
plt.xlabel('Valor de "dt"')
plt.ylabel('Cantidad')





#media=np.mean(coeficientes_ancho)
#N=len(coeficientes_ancho)
#w=bins[1]-bins[0]
#bins=bins[:-1]+w
#posicion_media=int(np.where((abs(coeficientes_ancho-media))==min(abs(coeficientes_ancho-media)))[0])
#Bmedio=coeficientes_ancho[posicion_media]
#integral=3
#a=1
#b=1
#while integral<0.95*N:
#    if abs(coeficientes_ancho[posicion_media-a]-Amedio)<abs(coeficientes_ancho[posicion_media+b]-Bmedio):
#        a+=1
#        integral+=1
#    if abs(coeficientes_ancho[posicion_media-a]-Amedio)>abs(coeficientes_ancho[posicion_media+b]-Bmedio):
#        b+=1
#        integral+=1
#
#error=(coeficientes_ancho[posicion_media+b]-coeficientes_ancho[posicion_media-a])/2
#print('El coeficiente de calibración de ancho es:',np.mean(coeficientes_ancho),'+-',error)
#plt.plot(np.linspace(coeficientes_ancho[posicion_media+b],coeficientes_ancho[posicion_media+b],100),np.linspace(0,max(n),100),'r--')
#plt.plot(np.linspace(coeficientes_ancho[posicion_media-a],coeficientes_ancho[posicion_media-a],100),np.linspace(0,max(n),100),'r--')

#coeficiente altura
coeficientes_altura=[]
for i in range(len(A)):
    if A[i]!=A[i-1]:
        coeficientes_altura.append(A[i])
coeficientes_altura=np.array(coeficientes_altura)

#coeficientes centrado en ese pico gigante de coeficientes        
coeficientes2_altura=[]
for i in range(len(coeficientes_altura)):
    if (1*10**9)>coeficientes_altura[i]>(0.93*10**9):
        coeficientes2_altura.append(coeficientes_altura[i])
        
plt.figure(num=1, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
n,bins,patches=plt.hist(coeficientes_altura,20,edgecolor='blue')
plt.title('Histograma de valores de la constante de calibración')
plt.xlabel('Valor de "A"')
plt.ylabel('Cantidad')

plt.figure(num=2, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
n,bins,patches=plt.hist(coeficientes2_altura,20,edgecolor='blue')
plt.title('Histograma de valores de la constante de calibración')
plt.xlabel('Valor de "A"')
plt.ylabel('Cantidad')
coeficientes2_altura=np.array(coeficientes2_altura)
coeficientes2_altura=coeficientes2_altura[coeficientes2_altura[:].argsort()]

media=np.mean(coeficientes2_altura)
N=len(coeficientes2_altura)
w=bins[1]-bins[0]
bins=bins[:-1]+w
posicion_media=int(np.where((abs(coeficientes2_altura-media))==min(abs(coeficientes2_altura-media)))[0])
Amedio=coeficientes2_altura[posicion_media]
integral=3
a=1
b=1
while integral<0.95*N:
    if abs(coeficientes2_altura[posicion_media-a]-Amedio)<abs(coeficientes2_altura[posicion_media+b]-Amedio):
        a+=1
        integral+=1
    if abs(coeficientes2_altura[posicion_media-a]-Amedio)>abs(coeficientes2_altura[posicion_media+b]-Amedio):
        b+=1
        integral+=1

error=(coeficientes2_altura[posicion_media+b]-coeficientes2_altura[posicion_media-a])/2
print('El coeficiente de calibración de altura es:',np.mean(coeficientes2_altura),'+-',error)
plt.plot(np.linspace(coeficientes2_altura[posicion_media+b],coeficientes2_altura[posicion_media+b],100),np.linspace(0,max(n),100),'r--')
plt.plot(np.linspace(coeficientes2_altura[posicion_media-a],coeficientes2_altura[posicion_media-a],100),np.linspace(0,max(n),100),'r--')

#plt.plot(np.arange(0,len(mediciones[0,:,0]),1),coeficientes,'b*')

