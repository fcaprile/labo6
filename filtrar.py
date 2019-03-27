# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:08:56 2019

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
import scipy.integrate as inte
from scipy.signal import filtfilt as filtro 
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from scipy import signal
import numpy as np
import pandas as pd
import scipy
carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/Mediciones_25-03/posta/'



indice=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        indice.append(archivo)
        
def filtro(y):
    fc = 0.1
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)
     
    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)
    
    s = list(y)
    new_signal = np.convolve(s, sinc_func)
    
    trace1 = go.Scatter(
        x=list(range(len(new_signal))),
        y=new_signal,
        mode='lines',
        name='Low-Pass Filter',
        marker=dict(
            color='#C54C82'
        )
    )
    
    layout = go.Layout(
        title='Low-Pass Filter',
        showlegend=True
    )
    
    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    py.iplot(fig, filename='fft-low-pass-filter')        




for j in range(1):#int(len(indice)/2)
    plt.figure(num=j, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    nombre=indice[j]
    data = pd.read_csv(carpeta+nombre, delimiter='  ',header = None)
    data=np.array(data)
    mediciones=np.zeros([len(data[:,0]),len(data[0,:])-1])
    plt.grid(True)
    t=data[:,0]
    for i in range(len(data[0,:])-1):
        mediciones[:,i]=data[:,i+1]
        
    y=mediciones[:,0]
    
    yint=[]
    
    
    plt.plot(t,filtro(y))    
