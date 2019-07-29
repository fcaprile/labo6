# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:43:02 2019

@author: DG
"""

import numpy as np
from matplotlib import pyplot as plt
import os
from numpy import genfromtxt
from scipy.integrate import cumtrapz as integrar


#falta multiplicar por la escala temporal de 2*10**6*10**-12s=2*10**-6s?
#va entre +-20+12? o entre +-15+12 us?
#no hace falta multiplicar y va entre +-20+12

#se asume que en todas las mediciones la sonda estaba correctamente medida en x10

#tiempo 800: 4 y 4,7us
#tiempo 1000: 3 y 4 ponele
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
        indice=[]
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".csv"):
                indice.append(archivo)
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

def curva_por_carpeta(carpeta_base):
    indice_carpetas=[]
    for carpeta in os.listdir(carpeta_base):
        indice_carpetas.append(carpeta)
#    print(indice_carpetas)
    corrientes=[]
    tensiones=[]
    corriente_media=[]
    tension_media=[]
    error_corriente_media=[]
    error_tension_media=[]
    for i in indice_carpetas:
        corrientes_esta_carpeta=[]
        tensiones_esta_carpeta=[]
        carpeta=carpeta_base+i+'/'
#        print(carpeta)
        indice=[]
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".csv"):
                indice.append(archivo)
#        print(indice)
        cant_mediciones_esta_carpeta=int(len(indice)/2)
        for j in range(cant_mediciones_esta_carpeta):   
            R=Csv(carpeta,2*j+1)
            bobina=Csv(carpeta,2*j,es_bobina=True)
            bobina.sacar_lineal()
            pico_bobina=bobina.encontrar_picos(0.8,distancia_entre_picos=100,valle=True)[0]
            tiempo0=bobina.x[pico_bobina]
            altura_pico_bobina=bobina.y[pico_bobina]
            bobina.x-=tiempo0
            R.x-=tiempo0
            t1=3*10**-6
            t2=4*10**-6
            tiempo=R.x
            pos1=posicion_x(tiempo,t1)
            pos2=posicion_x(tiempo,t2)
            altura_valle=np.mean(R.y[pos1:pos2])
            V=float(i)-altura_valle
            altura_valle/=-altura_pico_bobina #normalizo
            altura_valle*=568
            #y=filtrar(data)
            #promedio entre 4 y 4.7 us
            corrientes.append(altura_valle)
            corrientes_esta_carpeta.append(altura_valle)
            #restar caida sobre resistencia
            tensiones.append(V)
            tensiones_esta_carpeta.append(V)
        corriente_media.append(np.mean(corrientes_esta_carpeta))        
        tension_media.append(np.mean(tensiones_esta_carpeta))        
        error_corriente_media.append(np.std(corrientes_esta_carpeta))
        error_tension_media.append(np.std(tensiones_esta_carpeta))#/np.sqrt(len(corrientes_esta_carpeta)))
        print('Carpeta',i,'analizada!')
    
#    tensiones=[]
#    for i in indice_carpetas:
#        tensiones.append(float(i))    
    
    return tensiones,corrientes,tension_media,corriente_media,error_tension_media,error_corriente_media



def ajustar_entre(f,x,y,ey,xinf,xsup,escalax=1,escalay=1,color='g',label='Ajuste',plot=True):
    a=posicion_x(x,xinf)
    b=posicion_x(x,xsup)    
    y=y[a:b]
    x=x[a:b]
    ey=ey[a:b]
    popt, pcov = curve_fit(f,x,y,sigma =ey)
    if plot==True:
        xx=np.linspace(min(x),max(x),1000)                    
        plt.plot(xx*escalax,f(xx, *popt)*escalay, color=color, label = label)#los popt son los valores de las variables fiteadas que usara la funcion f                      
    return popt,pcov

def vector_entre(x,xinf,xsup):
    a=posicion_x(x,xinf)
    b=posicion_x(x,xsup)    
    return x[a:b]    

#%%
#analizo

carpeta_base1='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/Mediciones filtradas (saque las feas)/5-15/'
carpeta_base2='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/Mediciones filtradas (saque las feas)/5-22/'
carpeta_base3='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/Mediciones filtradas (saque las feas)/5-27/'
carpeta_base4='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/Mediciones filtradas (saque las feas)/6-3/'
#carpeta_base1='C:/Users/DG/Documents/GitHub/labo6_2/mediciones/Mediciones filtradas (saque las feas)/5-15/'
#carpeta_base2='C:/Users/DG/Documents/GitHub/labo6_2/mediciones/Mediciones filtradas (saque las feas)/5-22/'
#carpeta_base3='C:/Users/DG/Documents/GitHub/labo6_2/mediciones/Mediciones filtradas (saque las feas)/5-27/'
#carpeta_base4='C:/Users/DG/Documents/GitHub/labo6_2/mediciones/Mediciones filtradas (saque las feas)/6-3/'

t1,c1,tm1,cm1,et1,ec1=curva_por_carpeta(carpeta_base1)#,sacar_outliers=True)
t2,c2,tm2,cm2,et2,ec2=curva_por_carpeta(carpeta_base2)#,sacar_outliers=True)
t3,c3,tm3,cm3,et3,ec3=curva_por_carpeta(carpeta_base3)#,sacar_outliers=True)
t4,c4,tm4,cm4,et4,ec4=curva_por_carpeta(carpeta_base4)#,sacar_outliers=True)
#%%
#cargo txt
tensiones,corrientes,error_tensiones,error_corrientes=np.loadtxt('C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt/curva carac 800V entre 4 y 4.7.txt',delimiter='\t')


#%%
#ploteo todas las mediciones

tensiones=np.concatenate([t1,t2,t3,t4])
corrientes=np.concatenate([np.array(c1),c2,c3,c4])

A2=np.array([tensiones,corrientes])
A2=np.transpose(A2)
A2=A2[A2[:,0].argsort()]
A2=np.transpose(A2)#dificil de creer pero funciona
tensiones,corrientes=A2

corrientes-=y_dado_x(tensiones,corrientes,0)
corrientes/=1000 #lo convierto a corriente
carpeta_900V='C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt curvas carac/'
carpeta_900V='C:/Users/DG/Documents/GitHub/labo6_2/resultados/curva característica sonda doble Langmuir/txt curvas carac/'
tensiones8,corrientes8,error_corrientes8=np.loadtxt(carpeta_900V+'curva carac 8-5 entre 3,5 y 5 con error.txt',delimiter='\t')
#corrientes8*=568 #multiuplico por el valor medio de corriente de bobina
#corrientes8-=y_dado_x(tensiones8,corrientes8,0)
corrientes8/=1000
error_corrientes8/=1000

plt.plot(tensiones8,corrientes8*1000,'b*',label='Mediciones del 8/5')
plt.plot(tensiones,corrientes*1000,'g*',label='Mediciones del 15/5')#para que de rasonable dividi por 2... no encuentro el motivo de que sea necesario
plt.ylabel('Corriente (mA)')
plt.xlabel('Tensión (V)')
plt.grid()


plt.plot()

#np.savetxt('C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt/curva carac 800V entre 4 y 4.7.txt',[tensiones,corrientes,error_corrientes], delimiter='\t')
#%%
#ploteo mediciones promediadas
tensiones=np.concatenate([tm1,tm2,tm3,tm4])
corrientes=np.concatenate([cm1,cm2,cm3,cm4])
error_tensiones=np.concatenate([et1,et2,et3,et4])
error_corrientes=np.concatenate([ec1,ec2,ec3,ec4])

A2=np.array([tensiones,corrientes,error_corrientes,error_tensiones])
A2=np.transpose(A2)
A2=A2[A2[:,0].argsort()]
A2=np.transpose(A2)#dificil de creer pero funciona
tensiones,corrientes,error_corrientes,error_tensiones=A2

#corrientes-=y_dado_x(tensiones,corrientes,0)
corrientes/=1000#lo convierto a corriente 
error_corrientes/=1000
#carpeta_900V='C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt curvas carac/'
#carpeta_900V='C:/Users/DG/Documents/GitHub/labo6_2/resultados/curva característica sonda doble Langmuir/txt curvas carac/'
#tensiones8,corrientes8,error_tensiones8,error_corrientes8=np.loadtxt('curva carac 900V con t entre 0.7 y 3 sin outliers.txt',delimiter='\t')
##corrientes8*=568
##corrientes8-=y_dado_x(tensiones8,corrientes8,0)
#corrientes8/=1000
#error_corrientes8/=1000
#
#plt.plot(tensiones8,corrientes8*1000,'b*',label='Mediciones del 8/5')
#plt.errorbar(tensiones8,corrientes8*1000,error_corrientes8*1000,error_tensiones8,linestyle = 'None')
plt.plot(tensiones,corrientes*1000,'g*',label='Mediciones del 15/5')#para que de rasonable dividi por 2... no encuentro el motivo de que sea necesario
plt.errorbar(tensiones,corrientes*1000,error_corrientes*1000,linestyle = 'None')

plt.ylabel('Corriente (mA)')
plt.xlabel('Tensión (V)')
plt.grid()

#np.savetxt('curva carac 800V final.txt',[tensiones,corrientes,error_tensiones,error_corrientes], delimiter='\t')

#%%
#ajusto mediciones 800v

auxc=[]
auxt=[]
auxe=[]
for i in range(len(corrientes)):
    if np.isnan(corrientes[i])==False:
        auxc.append(corrientes[i])
        auxt.append(tensiones[i])
        auxe.append(error_corrientes[i])
auxc=np.array(auxc)
auxt=np.array(auxt)        
auxe=np.array(auxe)        
#a=posicion_x(auxt,-10)
#b=posicion_x(auxt,9)
#y=auxc[a:b]
#x=auxt[a:b]
#ey=auxe[a:b]
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit
vinf=-20
vsup=20
popt,pcov=ajustar_entre(f,auxt,auxc,auxe,vinf,vsup,escalay=1000)
#popt, pcov = curve_fit(f,x,y,sigma =ey)
#xx=np.linspace(min(x),max(x),1000)                    
#plt.plot(xx,f(xx, *popt)*1000, 'g-', label = 'Ajuste')#los popt son los valores de las variables fiteadas que usara la funcion f                      
Io=y_dado_x(auxt,auxc,vsup)
print('A orden simetrico, Te=',1/2/popt[0]*0.0008)

#%%
#ajuste asimetrico, hacemos 2 para compararlos
tensiones=np.concatenate([tm1,tm2,tm3,tm4])
corrientes=np.concatenate([np.array(cm1),cm2,cm3,cm4])*568#ver de dividir por 2 a c1...
error_tensiones=np.concatenate([et1,et2,et3,et4])
error_corrientes=np.concatenate([ec1,ec2,ec3,ec4])*568

A2=np.array([tensiones,corrientes,error_corrientes,error_tensiones])
A2=np.transpose(A2)
A2=A2[A2[:,0].argsort()]
A2=np.transpose(A2)#dificil de creer pero funciona
tensiones,corrientes,error_corrientes,error_tensiones=A2
plt.plot(tensiones,corrientes*1000,'g*',label='Mediciones del 15/5')#para que de rasonable dividi por 2... no encuentro el motivo de que sea necesario
plt.errorbar(tensiones,corrientes*1000,error_corrientes*1000,error_tensiones,linestyle = 'None')


#falto dividir por 1000 para que sea corriente pero como es una constante en comu al dividir ta too piola
vinfa=-17
vinfb=-7
vsupa=16
vsupb=6
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit

popta1,pcova1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-58,vinfa,escalay=1000,color='r',label='Ajuste con -17,16')
popta2,pcova2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupa,70,escalay=1000,color='r',label='Ajuste con -17,16')
poptb1,pcovb1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-58,vinfb,escalay=1000,color='r',label='Ajuste con -7,6')
poptb2,pcovb2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupb,70,escalay=1000,color='r',label='Ajuste con -7,6')
#agregar error en tensiones al ajustar?

Ie1a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta1)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
Ie2a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta2)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie1a,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie2a,'b*',label='Ie2')
plt.plot(vector_entre(tensiones,vinfa,vsupa),np.log(Ie1a/Ie2a),'b*',label='Ie1/Ie2')
pa,ea=curve_fit(f,vector_entre(tensiones,vinfa,vsupa),np.log(Ie1a/Ie2a))
plt.plot(vector_entre(tensiones,vinfa,vsupa),f(vector_entre(tensiones,vinfa,vsupa),*pa))
Tea=1/pa[0]
print('Contemplando la asimetria y con puntos de inflexion en',vinfa,'y',vsupa, ', Te=',"%.2f" %Tea)


Ie1b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb1)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])
Ie2b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb2)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie1b,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie2b,'b*',label='Ie2')
plt.plot(vector_entre(tensiones,vinfb,vsupb),np.log(Ie1b/Ie2b),'b*',label='Ie1/Ie2')
pb,eb=curve_fit(f,vector_entre(tensiones,vinfb,vsupb),np.log(Ie1b/Ie2b))
plt.plot(vector_entre(tensiones,vinfb,vsupb),f(vector_entre(tensiones,vinfb,vsupb),*pb))
Teb=1/pb[0]
print('Contemplando la asimetria y con puntos de inflexion en',vinfb,'y',vsupb, ', Te=',"%.2f" %Teb)

#%%
#metodo resistencia euivalente
tensiones=np.concatenate([tm1,tm2,tm3,tm4])
corrientes=np.concatenate([np.array(cm1),cm2,cm3,cm4])*568#ver de dividir por 2 a c1...
error_tensiones=np.concatenate([et1,et2,et3,et4])
error_corrientes=np.concatenate([ec1,ec2,ec3,ec4])*568

A2=np.array([tensiones,corrientes,error_corrientes,error_tensiones])
A2=np.transpose(A2)
A2=A2[A2[:,0].argsort()]
A2=np.transpose(A2)#dificil de creer pero funciona
tensiones,corrientes,error_corrientes,error_tensiones=A2

Vc=np.mean(corrientes[posicion_x(tensiones,-1):posicion_x(tensiones,1)])
Vc=0.3
vinfa=-17
vinfb=-7
vsupa=16
vsupb=6
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit

popta1,pcova1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-58,vinfa,plot=False,escalay=1000,color='r',label='Ajuste con -17,16')
popta2,pcova2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupa,70,plot=False,escalay=1000,color='r',label='Ajuste con -17,16')
poptb1,pcovb1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-58,vinfb,plot=False,escalay=1000,color='r',label='Ajuste con -7,6')
poptb2,pcovb2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupb,70,plot=False,escalay=1000,color='r',label='Ajuste con -7,6')
#agregar error en tensiones al ajustar?

Ie1a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta1)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
Ie2a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta2)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
Ie1b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb1)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])
Ie2b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb2)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])

plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie1a,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie2a,'g*',label='Ie2')
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie1b,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie2b,'g*',label='Ie2')


tensiones_entrea=vector_entre(tensiones,vinfa,vsupa)
tensiones_entreb=vector_entre(tensiones,vinfb,vsupb)

Ie10a=np.mean(Ie1a[posicion_x(tensiones_entrea,-2):posicion_x(tensiones_entrea,0.3)])
Ie20a=np.mean(Ie2a[posicion_x(tensiones_entrea,-2):posicion_x(tensiones_entrea,0.3)])
Ie10b=np.mean(Ie1b[posicion_x(tensiones_entreb,-2):posicion_x(tensiones_entreb,0.3)])
Ie20b=np.mean(Ie2b[posicion_x(tensiones_entreb,-2):posicion_x(tensiones_entreb,0.3)])

Tea=Vc/np.log(Ie10a/Ie20a)
Teb=Vc/np.log(Ie10b/Ie20b)

print('Metodo Req con',vinfa,'y',vsupa, ', Te=',"%.2f" %Tea)
print('Metodo Req con',vinfb,'y',vsupb, ', Te=',"%.2f" %Teb)


#%%
#ajusto mediciones 900v
#A2=np.array([tensiones8,corrientes8,error_corrientes8])
#A2=np.transpose(A2)
#A2=A2[A2[:,0].argsort()]
#A2=np.transpose(A2)#dificil de creer pero funciona
#tensiones8,corrientes8,error_corrientes8=A2
tensiones8,corrientes8,error_tensiones8,error_corrientes8=np.loadtxt('curva carac 900V con t entre 0.7 y 3 sin outliers.txt',delimiter='\t')
corrientes8*=568
#corrientes8-=y_dado_x(tensiones8,corrientes8,0)
corrientes8/=1000
error_corrientes8/=1000

auxc=[]
auxt=[]
auxe=[]
for i in range(len(corrientes8)):
    if np.isnan(corrientes8[i])==False:
        auxc.append(corrientes8[i])
        auxt.append(tensiones8[i])
        auxe.append(error_corrientes8[i])
auxc=np.array(auxc)
auxt=np.array(auxt)        
auxe=np.array(auxe)        
a=posicion_x(auxt,-40)
b=posicion_x(auxt,40)
y=auxc[a:b]
x=auxt[a:b]
ey=auxe[a:b]
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit
popt, pcov = curve_fit(f,x,y,sigma =ey)
plt.plot(tensiones8,corrientes8*1000,'b*',label='Mediciones del 8/5')
tensiones,corrientes,error_tensiones,error_corrientes=np.loadtxt('curva carac 800V final.txt',delimiter='\t')
plt.plot(tensiones,corrientes,'b*',label='Mediciones del 8/5')

xx=np.linspace(min(x),max(x),1000)                    
plt.plot(xx,f(xx, *popt)*1000, 'y-', label = 'Ajuste')#los popt son los valores de las variables fiteadas que usara la funcion f                      
print('A orden simetrico, Te=',1/2/popt[0]*0.00008)
#%%
#analisis 900V asimetrica
#falto dividir por 1000 para que sea corriente pero como es una constante en comu al dividir ta too piola
tensiones,corrientes,error_tensiones,error_corrientes=np.loadtxt('curva carac 900V con t entre 0.7 y 3 sin outliers.txt',delimiter='\t')

vinfa=-45
vinfb=-40
vsupa=48
vsupb=30
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit

popta1,pcova1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-70,vinfa,escalay=1000,color='r',label='Ajuste con -17,16')
popta2,pcova2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupa,70,escalay=1000,color='r',label='Ajuste con -17,16')
poptb1,pcovb1=ajustar_entre(f,tensiones,corrientes,error_corrientes,-70,vinfb,escalay=1000,color='r',label='Ajuste con -7,6')
poptb2,pcovb2=ajustar_entre(f,tensiones,corrientes,error_corrientes,vsupb,70,escalay=1000,color='r',label='Ajuste con -7,6')
#agregar error en tensiones al ajustar?

Ie1a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta1)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
Ie2a=abs(f(vector_entre(tensiones,vinfa,vsupa),*popta2)-corrientes[posicion_x(tensiones,vinfa):posicion_x(tensiones,vsupa)])
plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie1a,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfa,vsupa),Ie2a,'b*',label='Ie2')
plt.plot(vector_entre(tensiones,vinfa,vsupa),np.log(Ie1a/Ie2a),'b*',label='Ie1/Ie2')
pa,ea=curve_fit(f,vector_entre(tensiones,vinfa,vsupa),np.log(Ie1a/Ie2a))
plt.plot(vector_entre(tensiones,vinfa,vsupa),f(vector_entre(tensiones,vinfa,vsupa),*pa))
Tea=1/pa[0]
print('Contemplando la asimetria y con puntos de inflexion en',vinfa,'y',vsupa, ', Te=',"%.2f" %Tea)


Ie1b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb1)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])
Ie2b=abs(f(vector_entre(tensiones,vinfb,vsupb),*poptb2)-corrientes[posicion_x(tensiones,vinfb):posicion_x(tensiones,vsupb)])
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie1b,'b*',label='Ie1')
plt.plot(vector_entre(tensiones,vinfb,vsupb),Ie2b,'b*',label='Ie2')
plt.plot(vector_entre(tensiones,vinfb,vsupb),np.log(Ie1b/Ie2b),'b*',label='Ie1/Ie2')
pb,eb=curve_fit(f,vector_entre(tensiones,vinfb,vsupb),np.log(Ie1b/Ie2b))
plt.plot(vector_entre(tensiones,vinfb,vsupb),f(vector_entre(tensiones,vinfb,vsupb),*pb))
Teb=1/pb[0]
print('Contemplando la asimetria y con puntos de inflexion en',vinfb,'y',vsupb, ', Te=',"%.2f" %Teb)


#%% Comparacion sin analizar

tensiones8,corrientes8,error_corrientes8=np.loadtxt('curva carac 8-5 entre 3,5 y 5 con error.txt',delimiter='\t')
tensiones15,corrientes15,error_corrientes15=np.loadtxt('curva carac entre 3,5 y 5 con error.txt',delimiter='\t')

plt.plot(tensiones8,corrientes8,'b*',label='Mediciones del 8/5')
plt.errorbar(tensiones8,corrientes8,error_corrientes8,linestyle = 'None')
plt.plot(tensiones15,corrientes15/2,'g*',label='Mediciones del 15/5')#para que de rasonable dividi por 2... no encuentro el motivo de que sea necesario
plt.errorbar(tensiones15,corrientes15/2,error_corrientes15/2,linestyle = 'None')
plt.ylabel('Corriente')
plt.xlabel('Tensión (V)')
plt.grid()

