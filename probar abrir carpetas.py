# -*- coding: utf-8 -*-
"""
Created on Sun May 12 23:15:52 2019

@author: ferchi
"""
carpeta='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-8/'
indice=[]
for archivo in os.listdir(carpeta):
    indice.append(archivo)

np.savetxt('Curva caracteristica.txt',corrientes_promedio, delimiter = '\t')
d=np.loadtxt('Curva caracteristica.txt', delimiter = '\t')
