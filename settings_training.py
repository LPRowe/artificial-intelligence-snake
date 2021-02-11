# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:37:02 2020

@author: rowe1

Settings for ga_snake_train
"""

settings = {
        #(columns,rows) in the grid 
        'grid_size' : (10,10),
        
        'food_energy' : 100,
        
        #How many snakes in each generation  
        'population' : 500, 
        
        #how many generations to run for
        'generations' : 35,
        
        #Once a snake scores a score of fitness_threshold the training will stop
        'fitness_threshold' : 200,
        
        #Probability of a gene mutating
        'mutation_rate' : 0.0000,
        
        #mutation gaussian or uniform (other will assume uniform) gaussian adds np.random.normal() to mutated chromosomes
        'mutation_type' : 'gaussian',
        
        #range of values the mutated weight may become (this does not apply if mutation_type is 'gaussian')
        'mutation_range' : [-2,2],
        
        #survival_fraction=0.1 means the top 10% of snakes will be used to breed
        #and will continue on to the next round
        'survival_fraction' : 0.1,
        
        #nn_shape[0] is number of nodes in input layer, nn_shape[-1] is number of nodes in output layer
        #All hidden layers have nn_shape[1], nn_shape[2], ... nodes
        'nn_shape' : [18, 14, 8, 4], 
        
        #Activation function to be used at each layer (not including the input layer of course)
        'activation_functions' : ['relu','relu','sigmoid'],
        
        #if initial_config=True then the most recently trained model will be loaded as a start point for training
        'initial_config' : True,
        
        #set watch to True if you want the screen to display the game as the snakes are trained
        'watch' : False
            }