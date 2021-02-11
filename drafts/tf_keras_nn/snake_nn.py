# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:35:14 2020

@author: rowe1
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras

directions=['RIGHT','UP','LEFT','DOWN']

#Try assigning weight variable to layer 4
w=np.full((20,16),0.618)
b=np.full((16,),1.618)

model=keras.models.Sequential([
        keras.layers.Input(shape=(20,)),
        keras.layers.Dense(16,activation='relu',weights=[w,b]),
        keras.layers.Dense(12,activation='relu'),
        keras.layers.Dense(len(directions),activation='softmax')
        ])


print(model.weights[1])