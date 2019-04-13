# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 03:15:00 2019

@author: Publico
"""

from matplotlib import pyplot as plt
import visa
import numpy as np
import time
import os

rm=visa.ResourceManager()

class Osciloscopio:
    def __init__ (self, number):
        self.serial = rm.list_resources()[number]
        self.osci=rm.open_resource(self.serial)
        xze,xin,yze1,ymu1,yoff1=self.osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
        yze2,ymu2,yoff2=self.osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')         
        self.escala=xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
        
    def idn(self):
        return self.osci.query('*IDN?')
    
    def obtener_escalas(self):
        xze,xin,yze1,ymu1,yoff1=self.osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
        yze2,ymu2,yoff2=self.osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
        
        return xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2

    def medir_trigger_ambos_ch(self):
        self.osci.write('ACQuire:STATE RUN')
        self.osci.write('ACQuire:STOPAfter SEQuence')
        r=self.osci.query('ACQuire:STATE?')
        while r=='1\n':
            r=self.osci.query('ACQuire:STATE?')
            time.sleep(0.02)
        self.osci.write('DAT:SOU CH1' )
        data1=self.osci.query_binary_values('CURV?', datatype='B',container=np.array)
        self.osci.write('DAT:SOU CH2')    
        data2=self.osci.query_binary_values('CURV?', datatype='B',container=np.array)

        return data1,data2
    def medir(ch):
        xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
        yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
        self.osci.write('DAT:ENC RPB')
        self.osci.write('DAT:WID 1')
        self.osci.write('ACQuire:STATE RUN')
        self.osci.write('ACQuire:STATE STOP')#mejorar para que solo corra y pare
        self.osci.write('DAT:SOU CH{}'.format(ch) )
        data=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    
        return data
    
    def medir_ambos_ch(self):
        self.osci.write('ACQuire:STATE RUN')
        self.osci.write('ACQuire:STATE STOP')#mejorar para que solo corra y pare
        self.osci.write('DAT:SOU CH1' )
        data1=self.osci.query_binary_values('CURV?', datatype='B',container=np.array)
        self.osci.write('DAT:SOU CH2')    
        data2=self.osci.query_binary_values('CURV?', datatype='B',container=np.array)

        return data1,data2

    def escalar_ch(self,data,ch):
        xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=self.escala
        if ch==1:
            data=(data-yoff1)*ymu1+yze1
        if ch==2:
            data=(data-yoff2)*ymu2+yze2
            
        tiempo = xze + np.arange(len(data)) * xin
    
        return tiempo,data

    def escalar_ambos_ch(self,data1,data2):
        xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=self.escala
        data2=(data2-yoff2)*ymu2+yze2    
        tiempo = xze + np.arange(len(data1)) * xin
        data1=(data1-yoff1)*ymu1+yze1    
        
        return tiempo, data1, data2

        
    
#%%
o1=Osciloscopio(0)
o2=Osciloscopio(1)


N=5
mediciones_osc1=np.zeros([3,N,2500])
mediciones_osc2=np.zeros([3,N,2500])
dts=np.zeros(N)



print('A MEDIR!!')
#mido
for i in range(N):
    tiempo_inicio=time.time()
    data1,data2=o1.medir_ambos_ch()
    mediciones_osc1[1,i,:]=data1
    mediciones_osc1[2,i,:]=data2
    dts[i]=time.time()-tiempo_inicio
    data1=o2.medir__ch(1)
    mediciones_osc2[1,i,:]=data1
    if i%30==0 and i!=0:
        print('Se realizaron',i,'mediciones')

#ajusto con la escala
for i in range(N):
    tiempo_osc1,data1_osc1,data2_osc1=o1.escalar_ambos_ch(mediciones_osc1[1,i,:],mediciones_osc1[2,i,:])
    tiempo_osc2,data1_osc2=o2.escalar_ch(mediciones_osc2[1,i,:],1)
    tiempo_osc2-=dts[i]

    
    

if N<10:
    for i in range(N):
        plt.figure(num=i, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
        plt.plot(mediciones[0,i,:], mediciones[1,i,:]*1000,'b-')
        plt.plot(mediciones[0,i,:], mediciones[2,i,:],'r-')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Voltaje [V]')

Data1=np.zeros([1+N,2500])
Data1[0,:]=mediciones[0,0,:]
for i in range(N):
    Data1[i+1,:]=mediciones[1,i,:]
Data2=np.zeros([1+N,2500])
Data2[0,:]=mediciones[0,0,:]
for i in range(N):
    Data2[i+1,:]=mediciones[2,i,:]


carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/python/mediciones/4-3/'

np.savetxt(carpeta+'datoscanal1_punta100-'+str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+'-'+str(time.localtime()[3])+'-'+str(time.localtime()[4])+'.txt',Data1, fmt='%.18g', delimiter='\t', newline=os.linesep)
np.savetxt(carpeta+'datoscanal2_punta100-'+str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+'-'+str(time.localtime()[3])+'-'+str(time.localtime()[4])+'.txt',Data2, fmt='%.18g', delimiter='\t', newline=os.linesep)



#%%
#si se usan 2 canal para el osciloscopio 2:
for i in range(N):
    tiempo_inicio=time.time()
    data1,data2=o1.medir_ambos_ch()
    mediciones_osc1[1,i,:]=data1
    mediciones_osc1[2,i,:]=data2
    dts[i]=time.time()-tiempo_inicio
    data1,data2=o2.medir_ambos_ch()
    mediciones_osc2[1,i,:]=data1
    mediciones_osc2[2,i,:]=data2
    if i%30==0 and i!=0:
        print('Se realizaron',i,'mediciones')











#usar para medir ambos canales 1 sola vez:
#escala1=o1.preguntar_escala()
#escala2=o2.preguntar_escala()

#t,ch1=medir(1)
#t,ch2=medir(2)
#plt.plot(t,ch1*1000)
#plt.plot(t,ch2)
#tiempo,data1=medir(1)
#tiempo,data2=medir(2)

#metodo viejo antes de tipos de clases:

    
##print(osci.query('*IDN?'))
#def setup():
#    matriz_setup=np.zeros(2,8)
#    osci1.write('DAT:ENC RPB')
#    osci1.write('DAT:WID 1')
#    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
#    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
#    matriz_setup[0,:]=xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
#
#    osci2.write('DAT:ENC RPB')
#    osci2.write('DAT:WID 1')
#    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
#    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
#    matriz_setup[1,:]=xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
#
#    return matriz_setup
#    
#def medir_trigger():
#    osci.write('ACQuire:STATE RUN')
#    osci.write('ACQuire:STOPAfter SEQuence')
#    r=osci.query('ACQuire:STATE?')
#    while r=='1\n':
#        r=osci.query('ACQuire:STATE?')
#        time.sleep(0.02)
#    osci.write('DAT:SOU CH1' )
#    data1=osci.query_binary_values('CURV?', datatype='B',container=np.array)
#    osci.write('DAT:SOU CH2')    
#    data2=osci.query_binary_values('CURV?', datatype='B',container=np.array)
#    return data1,data2
#
#def medir1(ch):
#    osci1.write('DAT:SOU CH{}'.format(ch) )
#    data=osci1.query_binary_values('CURV?', datatype='B',container=np.array)
#    return data
#
#def medir2(ch):
#    osci2.write('DAT:SOU CH{}'.format(ch) )
#    data=osci2.query_binary_values('CURV?', datatype='B',container=np.array)
#    return data
    
#carpeta=path+day+'/'
#resource_name1=rm.list_resources()[0]#'USB0::0x0699::0x0363'*?
#resource_name2=rm.list_resources()[1]#'USB0::0x0699::0x0363'*?
#                                                                                                                                                                                                        
#
#osci1=rm.open_resource(resource_name1)
#osci2=rm.open_resource(resource_name2)
    
    
#matriz_setup=setup()
#setup1=matriz_setup[0,:]
#setup2=matriz_setup[1,:]


#    #para el osci 1
#    data1=mediciones[1,i,:]
#    data2=mediciones[2,i,:]    
#    xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=setup1
#    data2=(data2-yoff2)*ymu2+yze2    
#    tiempo = xze + np.arange(len(data1)) * xin
#    data1=(data1-yoff1)*ymu1+yze1    
#    mediciones[:,i,:]=tiempo,data1,data2
#    
#    #para el osci 2
#    data1=mediciones[1,i,:]
#    data2=mediciones[2,i,:]    
#    xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=setup2
#    data2=(data2-yoff2)*ymu2+yze2    
#    tiempo = xze + np.arange(len(data1)) * xin
#    data1=(data1-yoff1)*ymu1+yze1    
#    mediciones[:,i,:]=tiempo,data1,data2

