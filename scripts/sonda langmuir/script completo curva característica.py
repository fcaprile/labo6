import numpy as np
from scipy.signal import butter, lfilter, freqz,filtfilt
from matplotlib import pyplot as plt
import os


#falta multiplicar por la escala temporal de 2*10**6*10**-12s=2*10**-6s?
#va entre +-20+12? o entre +-15+12 us?
#no hace falta multiplicar y va entre +-20+12


#ver por que hace falta dividir por 2...

#falta ver de sacar mediciones muy diferentes


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

def y_dado_x(x,y,valorx):
    pos=posicion_x(x,valorx)
    return y[pos]

def curva_por_carpeta(carpeta_base,plotear=False):
    indice_carpetas=[]
    for nombre in os.listdir(carpeta_base):
        indice_carpetas.append(nombre)
    
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
            t1=3.5*10**-6
            t2=5*10**-6
            pos1=posicion_x(tiempo,t1)
            pos2=posicion_x(tiempo,t2)
            corrientes_matriz.append(np.mean(data[pos1:pos2]))
        corrientes.append(np.mean(corrientes_matriz))
        error_corrientes.append(np.std(corrientes_matriz)/np.sqrt(len(corrientes_matriz)))
        #    plt.figure(num= 0 , figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
            #plt.plot(tiempo, data, 'b-', label='data')
        #    plt.plot(bobina.x,bobina.y/1200)
        print('Carpeta',i,'analizada!')
    
    tensiones=[]
    for i in indice_carpetas:
        tensiones.append(float(i))    
    
    #plt.figure(num= 0 , figsize=(16, 11), dpi=80, facecolor='w', edgecolor='k')
    if plotear==True:
        tensiones=np.array(tensiones)
        error_corrientes=np.array(error_corrientes)
        corrientes=np.array(corrientes)
        plt.plot(tensiones,corrientes,'b*')
        plt.errorbar(tensiones,corrientes,error_corrientes,linestyle = 'None')
        plt.ylabel('Corriente')
        plt.xlabel('Tensión (V)')
        plt.grid()
    return tensiones,corrientes,error_corrientes
    
#%%
carpeta_base='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/5-8/'
indice_carpetas=[]
for nombre in os.listdir(carpeta_base):
    indice_carpetas.append(nombre)

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
        t1=3.5*10**-6
        t2=5*10**-6
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

plt.plot(tensiones8,corrientes8,'b*',label='Mediciones del 8/5')
plt.errorbar(tensiones8,corrientes8,error_corrientes8,linestyle = 'None')
plt.plot(tensiones15,corrientes15/2,'g*',label='Mediciones del 15/5')#para que de rasonable dividi por 2... no encuentro el motivo de que sea necesario
plt.errorbar(tensiones15,corrientes15/2,error_corrientes15/2,linestyle = 'None')
plt.ylabel('Corriente')
plt.xlabel('Tensión (V)')
plt.grid()

