# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:43:36 2019

@author: ferchi
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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
tensiones,corrientes,error_corrientes=np.loadtxt('C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt/curva carac 800V entre 4 y 4.7.txt',delimiter='\t')
#corrientes/=1000
#error_corrientes/=1000

#sacar outliers
tensiones=np.delete(tensiones,0)#si es .np
corrientes=np.delete(corrientes,0)#si es .np
error_corrientes=np.delete(error_corrientes,0)#si es .np
tensiones=np.delete(tensiones,7)#si es .np
corrientes=np.delete(corrientes,7)#si es .np
error_corrientes=np.delete(error_corrientes,7)#si es .np


plt.plot(tensiones,corrientes*1000,'b*',label='800 V')
plt.errorbar(tensiones,corrientes*1000,error_corrientes*1000,linestyle = 'None')
plt.ylabel('Corriente (mA)')
plt.xlabel('Tensión (V)')
plt.grid()

#hago los ajustes

f=lambda x,A,y0:A*x+y0

sat_neg=-26
sat_pos=35
p_sat_neg,cov_sat_neg=ajustar_entre(f,tensiones,corrientes,error_corrientes,tensiones[0],sat_neg,escalay=1000,plot=False)
p_sat_pos,cov_sat_pos=ajustar_entre(f,tensiones,corrientes,error_corrientes,sat_pos,tensiones[-1],escalay=1000,plot=False)

lin_neg=-5
lin_pos=6

#si hago 2 ajustes:
#p_lin_neg,cov_lin_neg=ajustar_entre(f,tensiones,corrientes,error_corrientes,lin_neg,0,escalay=1000,plot=False)
#p_lin_pos,cov_lin_pos=ajustar_entre(f,tensiones,corrientes,error_corrientes,0,lin_pos,escalay=1000,plot=False)
#x_plot=np.linspace(-20,0,100)
#plt.plot(x_plot,f(x_plot,*p_lin_neg)*1000,'g',label='Lineal')
#x_plot=np.linspace(0,15,100)
#plt.plot(x_plot,f(x_plot,*p_lin_pos)*1000,'g')

#si hago 1 solo ajuste
p_lin,cov_lin=ajustar_entre(f,tensiones,corrientes,error_corrientes,lin_neg,lin_pos,escalay=1000,plot=False)

x_plot=np.linspace(tensiones[0],-10,100)
plt.plot(x_plot,f(x_plot,*p_sat_neg)*1000,'r',label='Saturación')
x_plot=np.linspace(10,tensiones[-1],100)
plt.plot(x_plot,f(x_plot,*p_sat_pos)*1000,'r')

x_plot=np.linspace(-17,15,100)
plt.plot(x_plot,f(x_plot,*p_lin)*1000,'g',label='Lineal')
plt.legend(loc = 'best') 
#%%
#calculo temperatura electronica con funcion

#V_min, V_max son los valores entre los cuales se hara el calculo log
def Temp_elec_asim(tensiones,corrientes,error_corrientes,lin_neg,lin_pos,sat_neg,sat_pos,V_min,V_max,plot=True):

    f=lambda x,A,y0:A*x+y0
    #ajuste saturacion
    p_sat_neg,cov_sat_neg=ajustar_entre(f,tensiones,corrientes,error_corrientes,tensiones[0],sat_neg,escalay=1000,plot=False)
    p_sat_pos,cov_sat_pos=ajustar_entre(f,tensiones,corrientes,error_corrientes,sat_pos,tensiones[-1],escalay=1000,plot=False)
    #ajuste baja amplitud
    p_lin,cov_lin=ajustar_entre(f,tensiones,corrientes,error_corrientes,lin_neg,lin_pos,escalay=1000,plot=False)
        
    #analisis
#    Ii0_pos=p_sat_pos[1]
#    Ii0_neg=p_sat_neg[1]
    #Ii0=(abs(Ii0_pos)+abs(Ii0_neg))/2
    #
    #Te=1/2/p_lin[0]*Ii0
    #
    #print('Te =',Te)
    a=posicion_x(tensiones,V_min)
    b=posicion_x(tensiones,V_max)
    t_lin=tensiones[a:b]
    Ie1=abs(f(t_lin,*p_sat_pos)-corrientes[a:b])
    Ie2=abs(f(t_lin,*p_sat_neg)-corrientes[a:b])
    
    #propagacion de error:
    def error_lineal(xa,cov):
        error = np.sqrt(cov[1,1]+xa**2*cov[0,0]+2*xa*cov[0,1])
        return(error)
    
    Error_Ie1=error_lineal(t_lin,cov_sat_pos)+error_corrientes[a:b]
    Error_Ie2=error_lineal(t_lin,cov_sat_neg)+error_corrientes[a:b]
    
    Error_log=np.sqrt((1/Ie1*Error_Ie1)**2+(1/Ie2*Error_Ie2)**2)

    par_log,cov_log=curve_fit(f,t_lin,np.log(Ie1/Ie2),sigma=Error_log)
    Teb=1/par_log[0]
    Error_Teb=np.sqrt(cov_log[0,0])/par_log[0]**2
    print('Contemplando la asimetria, Te=',"%.2f" %Teb,'+-',"%.2f" %Error_Teb)
    
    
    if plot==True:
        plt.rcParams['font.size']=20#tamaño de fuente
        plt.figure(num=0, figsize=(9,6), dpi=80, facecolor='w', edgecolor='k')
        plt.subplots_adjust(left=0.14, bottom=0.13, right=0.98, top=0.98, wspace=None, hspace=None)
        plt.plot(tensiones,corrientes*1000,'b*',label='800 V')
        plt.errorbar(tensiones,corrientes*1000,error_corrientes*1000,linestyle = 'None')
        plt.ylabel('Corriente (mA)')
        plt.xlabel('Tensión (V)')
        plt.grid()

        x_plot=np.linspace(tensiones[0],sat_neg*0.2,100)
        plt.plot(x_plot,f(x_plot,*p_sat_neg)*1000,'r',label='Saturación')
        x_plot=np.linspace(sat_pos*0.2,tensiones[-1],100)
        plt.plot(x_plot,f(x_plot,*p_sat_pos)*1000,'r')
        
        x_plot=np.linspace(lin_neg*1.8,lin_pos*1.8,100)
        plt.plot(x_plot,f(x_plot,*p_lin)*1000,'g',label='Lineal')
        
        plt.figure(num=1, figsize=(9,6), dpi=80, facecolor='w', edgecolor='k')
        plt.subplots_adjust(left=0.14, bottom=0.13, right=0.98, top=0.98, wspace=None, hspace=None)
        plt.plot(t_lin,np.log(Ie1/Ie2),'b*',label='log(Ie1/Ie2)')
        plt.errorbar(t_lin,np.log(Ie1/Ie2),Error_log,linestyle = 'None')
        plt.plot(t_lin,f(t_lin,*par_log))
        plt.ylabel('log( Ie1 / Ie2 )')
        plt.xlabel('Tensión (V)')
        plt.grid()

#falta hacer propagacion de error... comming soon


#%%  Corro la funcion para analizar
       
tensiones,corrientes,error_corrientes=np.loadtxt('C:/Users/ferchi/Desktop/github labo 6/labo6/resultados/curva característica sonda doble Langmuir/txt/curva carac 800V entre 4 y 4.7.txt',delimiter='\t')
#corrientes/=1000
#error_corrientes/=1000

#sacar outliers
tensiones=np.delete(tensiones,0)#si es .np
corrientes=np.delete(corrientes,0)#si es .np
error_corrientes=np.delete(error_corrientes,0)#si es .np
tensiones=np.delete(tensiones,7)#si es .np
corrientes=np.delete(corrientes,7)#si es .np
error_corrientes=np.delete(error_corrientes,7)#si es .np
       
Temp_elec_asim(tensiones,corrientes,error_corrientes,-6,5,-26,35,-10,20)    
  

