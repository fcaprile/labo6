# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:50:40 2019

@author: Admin
"""
import numpy as np
import os
import time
path='C:/Users/Admin/Desktop/L6 Caprile Rosenberg/python/mediciones/'

day=str(time.localtime()[1])+'-'+str(time.localtime()[2])

os.mkdir(path+day)
os.mkdir(path+day+'/imagenes')


