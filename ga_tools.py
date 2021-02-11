# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:02:17 2020

@author: rowe1
"""

from __future__ import print_function

import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

def scale(arr,minimum=-2,maximum=2):
    ''' Scale a np.random.rand array to range from minimum to maximum'''
    return (arr-0.5)*(maximum-minimum)

def reporter(history, plot=True, savefile='./ga_snake_history/'):
    '''Prints statistics about the most recent population to monitor growth'''
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~GENERATION: '+str(len(history['best'])+1)+'~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

    print('Best:',str(round(history['best'][-1],2)))
    print('Average:',str(round(history['average'][-1],2)))
    print('Standard Deviation:',str(round(history['std'][-1],2)))
    print('Run Time:',str(round(history['run_time'][-1],2)))
    
    if plot:
        generations=np.linspace(1,len(history['best']),len(history['best']))
        best=history['best']
        average=history['average']
        std=history['std']
        
        average_std_over=[a+s for (a,s) in zip(average,std)]
        average_std_under=[a-s for (a,s) in zip(average,std)]
        
        plt.plot(generations,best,'r-',label='Best',lw=2)
        plt.plot(generations,average,'b-',label='Average',lw=2)
        plt.plot(generations,average_std_over,'g--',label='+1 STD')
        plt.plot(generations,average_std_under,'g--',label='-1 STD')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend(['Best','Average','+1 STD','-1 STD'],loc=2)
        plt.savefig(savefile+'progress_plot.png')

            
def mutate(nets, mutation_type='gaussian', mutation_range=[-2,2], mutation_rate=0.03, nn_shape=[24,30,30,4], activation_functions=['tanh','tanh','tanh','softmax']):
    if mutation_rate==0:
        return nets
    
    mutated_nets=[]
    
    for net in nets:
        #Flatten neural network to 1D list
        net = np.array(flatten_net(net))
        
        #use a list of booleans to denote whether a gene will be mutated
        mutate = np.random.rand(len(net)) <= mutation_rate
        
        if mutation_type=='gaussian':
            #Add a random value 
            gaussian_mutations = np.random.normal(size=len(net))

            net[mutate] += gaussian_mutations[mutate]
        else:
            #replace value with a random value
            for idx,result in enumerate(mutate):
                if result:
                    net[idx]=scale(np.random.rand(),minimum=mutation_range[0],maximum=mutation_range[1])
        
        #Rebuild the neural_network model from the flattened child net
        connection_weights,bias_weights = rebuild_net(net,nn_shape)
        mutated_net = make_nets(connection_weights,bias_weights,activation_functions)
        
        mutated_nets.append(mutated_net)
    
    return mutated_nets


def make_nets(connection_weights,bias_weights,activation_functions):
    ''' Each layer after the initial input layer of a densly connected FFNN 
    will have connection weights in the form of numpy array with the shape of 
    
    connection_weight_shape=(number_of_previous_layers_nodes,number_of_current_layers_nodes)
    
    there will also be one bias weight for each node in a layer with the shape of
    
    bias_weight_shape=(number_of_nodes_in_current_layer, )

    A densly connected NN will be made given weights for each connection and bias
    
    activation_functions should be given as a list where acceptable values are:
        'sigmoid','tanh','relu','softmax'
        
    Provide one array of connection_weights, one of bias_weights, and one activation
    function for each layer beyond the initial layer:
        
        i.e. for two hidden layers with 20 inputs, 12 hidden nodes, 8 hidden nodes, 4 output nodes:
            
            make_nets([np.random.rand(20,12),np.random.rand(12,8),np.random.rand(8,4)],
                       [np.random.rand(12,), np.random.rand(8,), np.random.rand(4,)],
                       ['tanh','tanh','softmax'])
            
            note, this is only for the first guess at the neural net weights.  After which,
            use the genetic algorithm to choose weights instead of using np.random.rand
    '''
    
    connections=[conn for conn in connection_weights]
    biases=[bias for bias in bias_weights]
    activations=[fcn for fcn in activation_functions]
    
    model=keras.models.Sequential([keras.layers.Input(shape=(connections[0].shape[0],))])
    
    for (c,b,a) in zip(connections,biases,activations):
        model.add(keras.layers.Dense(c.shape[1],weights=[c,b],activation=a))
    
    return model

def selection(nets,fitness, survival_fraction):
    '''Returns a zipped list of the top {survival_fraction} percent of neural
    networks based on their fitness'''
    
    agents=zip(nets,fitness)
    agents=sorted(agents, key=lambda agent: agent[1], reverse=True)
    
    #Return the top 20% of most fit agents to move on and breed    
    return agents[:int(survival_fraction*len(agents))]


def relu(x):
    '''Helper function for normalizing the fitness during crossover'''
    return x if x>0 else max(0.01, x+0.8)


def crossover(agents,nn_shape,activation_functions,population):
    child_nets=[]
    
    temp_fitness=[agent[1] for agent in agents]
    
    #Set all negative values to 0 in fitness
    temp_fitness=[relu(fit) for fit in temp_fitness]

    sum_fit=np.sum(temp_fitness)
    normalized_fitness=[fit/sum_fit for fit in temp_fitness]
    
    for i in range(int(0.5*(population-len(agents)))):
        #create one child each loop, until len(nets)+len(child_nets)=population
        
        #Select two parents giving higher probability of selection to the more fit snakes
        agent_index_1 = np.random.choice(len(agents),p=normalized_fitness)
        agent_index_2 = np.random.choice(len(agents),p=normalized_fitness)
        
        #Make sure the parents are not identical
        while agent_index_1 == agent_index_2:
            agent_index_2 = np.random.choice(len(agents),p=normalized_fitness)
        
        #Flatten parents neural_net weights (both connection and bias weights) to a 1D list for crossover
        parent_1 = flatten_net(agents[agent_index_1][0])
        parent_2 = flatten_net(agents[agent_index_2][0])
        
        #Fitness of each parent
        fitness_1 = agents[agent_index_1][1]
        fitness_2 = agents[agent_index_2][1]
        
        #Randomly select which parent the child gets its gene on while giving
        #a higher probability to the more fit parents genes
        try:
            probability_threshold = fitness_1 / (fitness_2 + fitness_1)
        except:
            #in the case that fitness_1+fitness_2=0
            probability_threshold = 0.5
        
        #If p1_genes is true, the child gets that gene from parent 1
        p1_genes = np.random.rand(len(parent_1)) <= probability_threshold
        
        child_1=np.array([0]*len(parent_1))
        child_2=np.array([0]*len(parent_1))

        child_gene_index=0
        for p1,p2,p1_gene in zip(parent_1,parent_2,p1_genes):
            if p1_gene:
                child_1[child_gene_index]=p1
                child_2[child_gene_index]=p2
            else:
                child_2[child_gene_index]=p1
                child_1[child_gene_index]=p2
            child_gene_index+=1
            
        
        #Rebuild the neural_network model from the flattened child net CHILD 1
        connection_weights, bias_weights = rebuild_net(child_1, nn_shape)
        child_net = make_nets(connection_weights, bias_weights, activation_functions)
        
        child_nets.append(child_net)
        
        #Rebuild the neural_network model from the flattened child net CHILD 2
        connection_weights, bias_weights = rebuild_net(child_2, nn_shape)
        child_net = make_nets(connection_weights, bias_weights, activation_functions)
        
        child_nets.append(child_net)
        
    return child_nets

def flatten_net(net):
    #Extract Numpy arrays of connection and bias weights from model
    layers=[layer.numpy() for layer in net.weights]
    
    #Convert each array to 1 dimension along the x-axis
    flat_layers=[np.reshape(layer,(-1,1)) for layer in layers]
    
    #Collect all connection andn bias weights into a list
    flattened_net=[]
    for layer in flat_layers:
        flattened_net.extend(layer)
        
    #convert all values to floats
    flattened_net=[float(weight) for weight in flattened_net]
        
    return flattened_net

def rebuild_net(flattened_net,nn_shape):
    '''
    Takes a list of the connection and bias weights in 1D form:
        List of all node connection weights for hidden layer 1
        List of all bias weights for hidden layer 1
        List of all node connedction weights for hidden layer 2
        ...
        List of all node connection weights for output layer
        List of all bias weights for output layer
    
    Restructures the flattened_net into arrays where each node layer
    has a 1D bias array and each connection layer has a 2D connection weight array
    
    the shape of each bias array is (number_of_nodes_in_layer,1)
    the shape of each connection weight array is (number_of_nodes_in_previous_layer,number_of_nodes_in_current_layer)
    
    
    i.e.: for a model with 3 input, 1 hidden layer of 2 nodes, and 1 output:
        
        connection_weights layer 1: 0.5, 0.7, -0.3, 0.4, 0.8, -0.6
        bias_weights layer 1: 0, 0
        connection_weights output layers: 0.8, -0.4
        bias_weights output layer: 0
        
        
    In : rebuild_net([0.5,0.7,-0.3,0.4,0.8,-0.6,0,0,0.8,-0.4,0])
    
    Out: ( list of connection weight numpy arrays, list of bias weight numpy arrays )
         ( [[[0.5,0.7,-0.3],[0.4,0.8,-0.6]], [0.8,-0.4]], [[0,0], [0]] )
    '''
    
    connection_weights=[]
    bias_weights=[]
    
    start_idx=0
    for idx in range(1,len(nn_shape)):
        #Add a reshaped layer to the connection_weights list
        end_idx=int(start_idx+nn_shape[idx-1]*nn_shape[idx])
        connection_weights.append(np.reshape(flattened_net[start_idx:end_idx],(nn_shape[idx-1], nn_shape[idx])))
        start_idx=end_idx
        
        #Add reshaped bias weights
        end_idx=int(start_idx+nn_shape[idx])
        bias_weights.append(np.reshape(flattened_net[start_idx:end_idx],(nn_shape[idx],)))
        start_idx=end_idx
        
    return (connection_weights,bias_weights)