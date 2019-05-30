# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:50:40 2019

@author: Admin
"""
import numpy as np
import os
import time
path='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/'
path='C:/Users/Admin/Desktop/labo6_Rosenberg_Caprile/mediciones/'
day=str(time.localtime()[1])+'-'+str(time.localtime()[2])

os.mkdir(path+day)
os.mkdir(path+day+'/imagenes')




#path='C:/Users/ferchi/Desktop/github labo 6/labo6/mediciones/mediciones removidas por ser diferentes/'
#for i in tensiones:
#    os.mkdir(path+str(i)+'/')
