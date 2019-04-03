from matplotlib import pyplot as plt
import visa
import numpy as np
import time
import os
rm=visa.ResourceManager()
carpeta='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/python/mediciones/4-3/'
#carpeta=path+day+'/'
resource_name=rm.list_resources()[0]#'USB0::0x0699::0x0363'*?
                                                                                                                                                                                                        

osci=rm.open_resource(resource_name)
        
#print(osci.query('*IDN?'))
def setup():
    osci.write('DAT:ENC RPB')
    osci.write('DAT:WID 1')
    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
    return xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
    
def medir_trigger():
    osci.write('ACQuire:STATE RUN')
    osci.write('ACQuire:STOPAfter SEQuence')
    r=osci.query('ACQuire:STATE?')
    while r=='1\n':
        r=osci.query('ACQuire:STATE?')
        time.sleep(0.02)
    osci.write('DAT:SOU CH1' )
    data1=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    osci.write('DAT:SOU CH2')    
    data2=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    return data1,data2

def medir(ch):
    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
    osci.write('DAT:ENC RPB')
    osci.write('DAT:WID 1')
    osci.write('DAT:SOU CH{}'.format(ch) )
    data=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    if ch==1:
        data=(data-yoff1)*ymu1+yze1
    if ch==2:
        data=(data-yoff2)*ymu2+yze2
        
    tiempo = xze + np.arange(len(data)) * xin

    return tiempo,data

    
#%%
N=500
mediciones=np.zeros([3,N,2500])
parametros=np.zeros([8,N])
xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=setup()

print('A MEDIR!!')
for i in range(N):
    data1,data2=medir_trigger()
    mediciones[1,i,:]=data1
    mediciones[2,i,:]=data2
    if i%30==0 and i!=0:
        print('Se realizaron',i,'mediciones')
for i in range(N):
    data1=mediciones[1,i,:]
    data2=mediciones[2,i,:]
    data2=(data2-yoff2)*ymu2+yze2    
    tiempo = xze + np.arange(len(data1)) * xin
    data1=(data1-yoff1)*ymu1+yze1    
    mediciones[:,i,:]=tiempo,data1,data2

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



np.savetxt(carpeta+'datoscanal1_punta100-'+str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+'-'+str(time.localtime()[3])+'-'+str(time.localtime()[4])+'.txt',Data1, fmt='%.18g', delimiter='\t', newline=os.linesep)
np.savetxt(carpeta+'datoscanal2_punta100-'+str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+'-'+str(time.localtime()[3])+'-'+str(time.localtime()[4])+'.txt',Data2, fmt='%.18g', delimiter='\t', newline=os.linesep)


#usar para medir ambos canales 1 sola vez

#t,ch1=medir(1)
#t,ch2=medir(2)
#plt.plot(t,ch1*1000)
#plt.plot(t,ch2)
#tiempo,data1=medir(1)
#tiempo,data2=medir(2)
