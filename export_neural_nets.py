# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:01:47 2020

@author: rowe1
"""

import os
import tensorflow as tf
from tensorflow import keras
import glob
from ga_tools import *
import settings_playback
settings=settings_playback.settings

best_snakes_file = settings['best_snakes_file']
nn_shape = settings['nn_shape']

nets = []
weights = {}

#load best neural net for each generation
net_files=glob.glob(best_snakes_file+'//*')
net_files=[i.split('\\')[-1] for i in net_files]
    
#Order files by generation
net_files=sorted(net_files,key=lambda name: int(name.split('_')[0]))

#Manually compile the top 50 neural nets from previous session
for file in net_files[-5:]:
    print()
    net=keras.models.load_model(best_snakes_file+'//'+file)
    flattened_net=flatten_net(net)
    connection_weights,bias_weights=rebuild_net(flattened_net,nn_shape)
    
    #Create a dictionary of net weights
    weights[file.split('_')[0]] = [connection_weights, bias_weights]
    
    #nets.append(make_nets(connection_weights,bias_weights,activation_functions))
    print()
    print('Manually loading, flattening, and rebuilding neural net',file,'from checkpoint.')

    print('nets')
