# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:18:00 2018

@author: zhou
"""
import pickle
filename = 'urls.txt' 
with open(filename,"rb") as f:
    data=pickle.load(f) 