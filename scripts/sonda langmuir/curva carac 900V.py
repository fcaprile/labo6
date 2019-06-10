# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:22:56 2019

@author: DG
"""

#los picos se ven entre 0.7 y 3 us. razon: desconocida... sera que la escala temporal es la mitad??

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
            #y=filtrar(data)
            #promedio entre 4 y 4.7 us
            t1=0.7*10**-6
            t2=3*10**-6
            pos1=posicion_x(tiempo,t1)
            pos2=posicion_x(tiempo,t2)
            corr=np.mean(data[pos1:pos2])
            corrientes.append(corr)
            corrientes_esta_carpeta.append(corr)
            #restar caida sobre resistencia
            V=float(i)-np.mean(R.y[pos1:pos2])
            tensiones.append(V)
            tensiones_esta_carpeta.append(V)
        corriente_media.append(np.mean(corrientes_esta_carpeta))        
        tension_media.append(np.mean(tensiones_esta_carpeta))        
        error_corriente_media.append(np.std(corrientes_esta_carpeta)/np.sqrt(len(corrientes_esta_carpeta)))
        error_tension_media.append(np.std(tensiones_esta_carpeta))#/np.sqrt(len(corrientes_esta_carpeta)))
        print('Carpeta',i,'analizada!')
    
#    tensiones=[]
#    for i in indice_carpetas:
#        tensiones.append(float(i))    
    
    return tensiones,corrientes,tension_media,corriente_media,error_tension_media,error_corriente_media

#%%
carpeta_base900='C:/Users/DG/Documents/GitHub/labo6_2/mediciones/Mediciones filtradas (saque las feas)/5-8/'
tensiones_todas,corrientes_todas,tensiones,corrientes,error_tensiones,error_corrientes=curva_por_carpeta(carpeta_base900)#,sacar_outliers=True)
A2=np.array([tensiones,corrientes,error_tensiones,error_corrientes])
A2=np.transpose(A2)
A2=A2[A2[:,0].argsort()]
A2=np.transpose(A2)#dificil de creer pero funciona
tensiones,corrientes,error_tensiones,error_corrientes=A2
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
a=posicion_x(auxt,0)
b=posicion_x(auxt,43)
y=auxc[a:b]
x=auxt[a:b]
ey=auxe[a:b]
f=lambda x,A,y0: A*x+y0
from scipy.optimize import curve_fit
popt, pcov = curve_fit(f,x,y,sigma =ey)
plt.plot(tensiones,corrientes*1000,'g*',label='Mediciones del 8/5')

xx=np.linspace(min(x),max(x),1000)                    
plt.plot(xx,f(xx, *popt)*1000, 'y-', label = 'Ajuste')#los popt son los valores de las variables fiteadas que usara la funcion f                      
plt.errorbar(tensiones,corrientes*1000,error_corrientes*1000,error_tensiones,linestyle = 'None')
plt.ylabel('Corriente (mA)')
plt.xlabel('Tensión (V)')
plt.grid()
print('A orden simetrico, Te=',1/2/popt[0]*y[-1])
plt.legend(loc = 'best') 
    
#np.savetxt('curva carac 900V con t entre 0.7 y 3 sin outliers.txt',[tensiones,corrientes,error_tensiones,error_corrientes], delimiter='\t')
#%%
tensiones8,corrientes8,error_tensiones8,error_corrientes8=np.loadtxt('curva carac 900V con t entre 0.7 y 3 sin outliers.txt',delimiter='\t')
corrientes8*=568
#corrientes8-=y_dado_x(tensiones8,corrientes8,0)
corrientes8/=1000
error_corrientes8/=1000

