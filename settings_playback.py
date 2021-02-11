# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:15:13 2020

@author: rowe1
"""

settings = {
        #(columns,rows) in the grid 
        'grid_size' : (20,20),
        
        'food_energy' : 100,
        
        #nn_shape[0] is number of nodes in input layer, nn_shape[-1] is number of nodes in output layer
        #All hidden layers have nn_shape[1], nn_shape[2], ... nodes
        'nn_shape' : [18, 14, 8, 4], 
        
        #Activation function to be used at each layer (not including the input layer of course)
        'activation_functions' : ['relu','relu','sigmoid'],
        
        #Location of the best performing neural nets from each generation
        'best_snakes_file' : './ga_snake_history/best',
        
        #set watch to True if you want the screen to display the game as the snakes are trained
        'watch' : True,
        
        #auto-play=True : when a snake dies, the next generation snake will start to play
        #auto-play=False: key input will be used to change generations
        'autoplay' : False,
        
        #Set the speed of the game with clock speed
        'clock_speed' : 15,
        
        #If colorful then snake will be rainbow colored, otherwise the snake and food will be green
        'colorful' : False,
        
        #Choose how many generations back to see 10 will show only the top 10 snakes
        #If play_top_n_gen = 0 all generations will be loaded
        'play_top_n_gen' : 10,
        
        'basic_instincts' : True
            }