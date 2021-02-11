# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:24:35 2020

@author: Logan Rowe
"""

from __future__ import print_function

import pygame
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import pickle
import time
import matplotlib.pyplot as plt
import glob
import gc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

pygame.init()


# =============================================================================
# INPUT VALUES FOR NEURAL NETWORK ARE OUTPUT VALUES FROM WHAT SNAKE SEES
# =============================================================================

def snakeVision(snake,food,obstruction_connections=False):
    '''
    Takes the snake of interest and current food as inputs returns an output
    of 20 values that the snake sees and a list of the locations of obstructions.
    
    The output will be fed as input to the neural net.  The list of obstructions
    will be used visualize what the snake sees as it moves (plot red spots on 
    obstruction locations).
    
    All distances are normalized to range between -1 and 1 where -1 represents
    a wall that is 30 blocks (the width of the screen) to the left or above the
    snakes head and 1 for 30 blocks to the right or below the snakes head
    
        note: this does not account for diagonal distances being root(2) times
        longer than horizontal or vertical distances... should only be of
        minor concern
    
    This in combination with the us of tanh as an activation function should
    assist in speeding up the training process
    
    If two observation points are connected by a series of obstructions it will
    be denoted by 1, if they are not connected -1
    
        i.e. Determine whether obstriction at right is connected to obstruction 
             at up-right by a chain of obstructions (i.e. right is wall and 
             upright is also wall)=1 or (i.e. right is tail not touching wall 
             and up right is wall)=-1
    
    
    outputs=[x dist from snakes head to food,
             y dist from snakes head to food,
             is food to the right of the snake,
             is food above the snake,
             is food to the left of the snake,
             is food below the snake,
             dist to nearest obstruction to the right,
             dist to nearest obstruction to the up-right,
             dist to nearest obstruction to the up,
             dist to nearest obstruction to the up-left,
             dist to nearest obstruction to the left,
             dist to nearest obstruction to the down-left,
             dist to nearest obstruction to the down,
             dist to nearest obstruction to the downright,
             snake is headed to the right 1 for true 0 for false
             snake is headed up 1 for true 0 for false
             snake is headed to the left 1 for true 0 for false
             snake is headed down 1 for true 0 for false
             ]    
    '''
    
    outputs=[]
    
    #Add Food location x distance and y distance (consistently using final position - initial position)
    outputs.append(food.position[0]-snake.components[0].position[0])
    outputs.append(food.position[1]-snake.components[0].position[1])    
    
    inline_with_food = False
    if inline_with_food:
        #Add 1 if food is in line with snake (right, above, left, or down)
        outputs.append(grid_rows if (snake.components[0].position[1]==food.position[1] and snake.components[0].position[0]<food.position[0]) else 0)
        outputs.append(grid_rows if (snake.components[0].position[0]==food.position[0] and snake.components[0].position[1]>food.position[1]) else 0)
        outputs.append(grid_rows if (snake.components[0].position[1]==food.position[1] and snake.components[0].position[0]>food.position[0]) else 0)
        outputs.append(grid_rows if (snake.components[0].position[0]==food.position[0] and snake.components[0].position[1]<food.position[1]) else 0)
    else:
        #If food is to the right, above, left or below the snake (does not need to be direct) 1
        #i.e. if the food is above and to the left of the snake then [0,1,1,0]
        #i.e. if the food is to the right and below the snake then [1,0,0,1]
        #i.e. if the food is directly above the snake then [0,1,0,0]
        outputs.append(grid_rows if snake.components[0].position[0]<food.position[0] else 0)
        outputs.append(grid_rows if snake.components[0].position[1]>food.position[1] else 0)
        outputs.append(grid_rows if snake.components[0].position[0]>food.position[0] else 0)
        outputs.append(grid_rows if snake.components[0].position[1]<food.position[1] else 0)
        
        
    #locate obstructions (snake's tail or wall) in 8 directions 
    #[right, up-right, up, up-left, left, down-left, down, down-right]
    obstructions=[]
    
    #Positions currently inhabited by snake body
    snake_space=set(tuple(snake.snake_space()[1:]))
    
    #Position of the snakes head
    x_naught,y_naught=severus.components[0].position[0],severus.components[0].position[1]
    
    #Helper dictionary for finding nearest obstruction in a given direction
    #Add the following (x,y) values when incrementing directions start right 
    #and go CCW (note: down is positive up is negative)
    direction_dict={'dir0':(1,0),'dir1':(1,-1),'dir2':(0,-1),'dir3':(-1,-1),
                    'dir4':(-1,0),'dir5':(-1,1),'dir6':(0,1),'dir7':(1,1)}
        
    #Find the nearest obstruction in direction ___ and note how far away it is
    #from the snakes head
    for direction in direction_dict:
        x,y=x_naught,y_naught
        dist=0
        while (x>=0 and x<=grid_columns-1) and (y>=0 and y<=grid_rows-1) and ((x,y) not in snake_space):
            x+=direction_dict[direction][0]
            y+=direction_dict[direction][1]
            dist+=1
        obstructions.append(tuple((x,y)))
        outputs.append(dist)
    
    #Determine whether obstriction at right is connected to obstruction at up-right
    #by a chain of obstructions (i.e. right is wall and upright is also wall)=1
    # or (i.e. right is tail not touching wal and up right is wall)=-1
        
    #add another copy of the obstruction to the right, to the end of the list
    obstructions.append(obstructions[0])
    
    if obstruction_connections:
        #check if each obstruction is connected to the one located CCW from it
        for idx,obstruction in enumerate(obstructions[:-1]):
            
            if (obstruction not in snake_space) and (obstructions[idx+1] not in snake_space):
                
                #if both obstructions are on the wall, then yes they are connected
                outputs.append(grid_rows) #will be normalized with other distances later
                
            elif (obstruction in snake_space) and (obstructions[idx+1] in snake_space):
                
                #if both obstructions are on the snake's body, then yes they are connected
                outputs.append(grid_rows)
                
            else:
                snake_is_touching_wall=False
                #If a part of the snake is adjacent to the wall, then yes they are connected
                for position in snake_space:
                    x,y=position
                    if (x<1 or x>=grid_columns-1) or not (y<2 or y>grid_rows-1):
                        snake_is_touching_wall=True
                
                if snake_is_touching_wall:
                    outputs.append(grid_rows)
                else:
                    #Snake is not touching the wall
                    outputs.append(-grid_rows)
    
    #Lastly lets tell the snake what direction it is currently headed:
    #horizontal: (-1,0) --> -1 | (1,0) --> 1  | (0,+/- 1) --> 0
    #vertical: (-1,0) --> 0 | (1,0) --> 0  | (0,+/- 1) --> +/- 1  
    outputs.append(grid_rows if snake.direction[0]==1 else 0) #heading right
    outputs.append(grid_rows if snake.direction[1]==-1 else 0) #heading upward
    outputs.append(grid_rows if snake.direction[0]==-1 else 0) #heading left
    outputs.append(grid_rows if snake.direction[1]==1 else 0) #heading downward
        
    
    #Normalize ouputs
    outputs=[output/grid_rows for output in outputs]
        
    return (outputs,obstructions)

def drawObstructions(obstructions):
    '''
    Obstructions are given from snake vision, they are (x,y) pairs of locations
    that will cause the snake to die if touched
    
    drawObstructions([(1,2),(7,9),(30,5),...])
    will blit a red square anywhere that is hazardous to the snake
    '''
    
    #Plot a red square slightly larger than the grid square size at each location
    marker_size=0.5
    square_width,square_height=marker_size*grid.square_width,marker_size*grid.square_height
    
    for obstruction in obstructions:
        color=(255,0,0)

        x,y=obstruction
        x1,y1=grid.x+x*grid.square_width,grid.y+y*grid.square_height
        
        if x==grid_columns:
            x1-=grid.square_width-square_width
        elif x==-1:
            x1+=grid.square_width
        elif y==grid_rows:
            y1-=square_height
        elif y==-1:
            y1+=grid.square_height
        else:
            x1+=int(0.5*(grid.square_width-square_width))
            y1-=int(0.5*(2*grid.square_width-square_height))
            color=(255,255,255)
            
        pygame.draw.rect(win,color,(x1,y1,square_width,square_height),0)
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    
    pygame.draw.rect(win,(0,0,0),(0,0,win_width,win_height))
    
    grid.draw(win)
    severus.draw(win,grid)
    food.draw(win,grid)
    header.draw(win,win_width,severus.energy,snake_icon)
    
    drawObstructions(obstructions)
    
    pygame.display.update()

# =============================================================================
# INITIAL CONDITIONS FOLLOWED BY RUN LOOP
# =============================================================================

def evalGenomes(population, generations, mutation_type='gaussian', food_energy=300, grid_size=(10,10), survival_fraction=0.1, fitness_threshold=200, mutation_rate=0.03, mutation_range=[-2,2], nn_shape=[24,30,30,4], activation_functions=['tanh','tanh','tanh','softmax'], initial_config=False, watch=False):
    '''
    population: the number of snakes in each generation
    generations: the number of generations you wish to run the evolution process for
    
    mutation rate: probability of a gene mutating
    mutation_range: the min and max possible mutated value
    nn_shape: the shape of the neural net: input layer, hidden 1, hidden 2, ..., output
    activation_functions: the function that will be used at layer1, layer2, ..., output
    
    initial_config: If False, the neural network will initiate with random weights on generation 1
                    If initial_config='configuration_file_name.pkl' then neural net will use
                    the weights from the pkl file, thus starting from a partially evolved state
    
    '''
    
    # =============================================================================
    # MAIN LOOP
    # =============================================================================
    '''From here until the run loop is simply initializing game objects such as
    the snake population, the board, food, etc.  
    '''
    
    #objects
    global grid, win, severus, food, header
    
    #dimensions
    global grid_rows,grid_columns, win_width, win_height
    
    #flags and values
    global colors, game_on, snake_icon, obstructions, snake_output, gen
    
    gen=0
    
    #SET INITIAL CONDITIONS
    if watch:
        clock=pygame.time.Clock()
        clock.tick(10)
        pygame.time.delay(100)
    win_width=500
    win_height=win_width+50
    if watch:
        win=pygame.display.set_mode((win_width,win_height))
    
    
    #Size of grid for snake to move on
    grid_columns,grid_rows=grid_size
    
    #Range of colors to randomly choose from for snake food
    color_dict={'red':(255,0,0),
            'orange':(255,127,0),
            'yellow':(255,255,0),
            'green':(0,255,0),
            'blue':(0,0,255),
            'indigo':(75,0,130),
            'violet':(148,0,211)}
    
    colorful=True
    if colorful:
        colors=['red','orange','yellow','green','blue','indigo','violet']
    else:
        colors=['green']
    
    
    #flag for whether the snake is alive
    game_on=True


    #CREATE INITIAL OBJECTS
    #Square grid the same width as the window
    grid=GridBoard(grid_columns,grid_rows,win_width,win_width,(0,win_height-win_width))
    
    
    #Snake
    severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)
    
    
    #Score Board Snake Icon Resized to fit scoreboard
    snake_icon=pygame.image.load('./images/snake-image-alpha-removed.png')
    snake_icon_ratio=1280/960
    snake_icon=pygame.transform.scale(snake_icon,(int(snake_icon_ratio*0.75*(win_height-win_width)),int(0.75*(win_height-win_width))))
    
    
    #Score Board
    header=ScoreBoard(severus.length(),(win_width,win_height-win_width),win_width,snake_icon)
    

    #Add food to the map in a location that the snake does not inhabit
    food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
    while food_loc in severus.snake_space():
        food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],shape=severus.components[0].shape,grid=grid)

    

    # =============================================================================
    # CREATE FIRST POPULATION OF SNAKES AND NEURAL NETWORKS
    # =============================================================================
    #record the history of the performance of each generation of snakes
    history={'best' : [],
             'average' : [],
             'std' : [],
             'run_time' : []
             }
    
    nets = []
    snakes = []
    fitness = [0]*population
    
    #if no initial_configuration file is given, randomly generate neural net weights
    if not initial_config:
        for i in range(population):
            snakes.append(Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy))
            
            #weights for connections between nodes
            conn_weights=[scale(np.random.rand(nn_shape[idx],nn_shape[idx+1])) for idx in range(len(nn_shape)-1)]
            
            #bias for each node
            bias_weights=[scale(np.random.rand(nn_shape[idx+1],)) for idx in range(len(nn_shape)-1)]
            
            #create neural net with given weights and activation functions
            nets.append(make_nets(conn_weights,bias_weights,activation_functions))
    else:
        #build population of snakes
        for i in range(population):
            snakes.append(Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy))
        
        #load top 50 nerual nets from previous session
        net_files=glob.glob('ga_snake_history/checkpoint_weights/*.h5')
        net_files=[i.split('\\')[-1] for i in net_files]
        
        nets=[]
        #Manually compile the top 50 neural nets from previous session
        for file in net_files:
            print()
            net=keras.models.load_model('./ga_snake_history/checkpoint_weights/'+file)
            flattened_net=flatten_net(net)
            connection_weights,bias_weights=rebuild_net(flattened_net,nn_shape)
            nets.append(make_nets(connection_weights,bias_weights,activation_functions))
            print()
            print('Manually loading, flattening, and rebuilding neural net',file,'from checkpoint.')

        
        #Reload the latest history
        with open('./ga_snake_history/history.pkl', 'rb') as file:
            history = pickle.load(file)
            
        #if the population is larger than 50, expand on the loaded neural nets to fill the population
        for i in range(population-len(nets)):
            nets.append(np.random.choice(nets))   
        
        print('nets')
        print(len(nets))


            
    #Decide how much the snake should be rewarded for each positive/negative action
    reward_food = 2
    reward_move = 0.01
    reward_hit_wall = - 0
    
    for gen in range(generations):
        t_start=time.time()
        gen+=1
        
        #Delete unreferenced objects
        gc.collect()

        #run loop
        snake_count=0
        for index,severus in enumerate(snakes):
            
            #Progress bar
            if snake_count%100==0:
                empty=' '*50
                full='|'*50
                progress=float(snake_count)/float(population)
                print('|'+full[:int(progress*50)]+empty[:int((1-progress)*50)]+'|')
            snake_count+=1

            run=True                
            while run:
            
                #Set the speed the game runs at playing: (50,20) | training (0,comment out)
                if watch:
                    pygame.time.delay(50)
                    clock.tick(15)
                
                #Every time step, severus loses one energy [kcal]
                severus.energy-=1
                
                #get list of all events that happen i.e. keyboard, mouse, ...
                for event in pygame.event.get():
                    #Check if the red X was clicked
                    if event.type==pygame.QUIT:
                        run=False
                
                #keep track of where the snakes tail is before movement incase it eats food
                severus.tail=severus.components[-1]
                
                
                # =============================================================================
                # CONTROL SNAKE USING NEURAL NET      
                # =============================================================================
                #Increase the snakes fitness for each frame it has lived 
                severus.fitness += reward_move
                
                #Output the snake vision to the neural net
                snake_output,obstructions = snakeVision(severus,food)
                
                
                snake_output=np.reshape(np.array(snake_output),(1,-1))
                
                #Ask neural net what snake should do based on snake's vision
                nn_output = nets[index].predict(snake_output)
                                
                #Perform action suggested by nn_output
                snake_actions={0:'RIGHT',1:'UP',2:'LEFT',3:'DOWN',4:'NONE'}
                
                #OUTPUT FROM NEURAL NET (NN_OUTPUT) DRIVES THE SNAKE
                if (snake_actions[np.argmax(nn_output)]=='LEFT' and severus.direction!=(1,0)):
                    #Only allow a left turn if the snake is not going right
                    
                    #Update the snakes tail components position to be to the left of the snakes head This will create the illusion of the snake progressing forward
                    severus.components[-1].position=(severus.components[0].position[0]-1,severus.components[0].position[1])
                    #Move the tail component to the head position of the snake
                    severus.components=[severus.components.pop()]+severus.components
                    #Change the direction of the snake to left
                    severus.direction=(-1,0)
                    
                    
                if (snake_actions[np.argmax(nn_output)]=='RIGHT' and severus.direction!=(-1,0)):
                    severus.components[-1].position=(severus.components[0].position[0]+1,severus.components[0].position[1])
                    severus.components=[severus.components.pop()]+severus.components
                    severus.direction=(1,0)
                    
                if (snake_actions[np.argmax(nn_output)]=='UP' and severus.direction!=(0,1)):
                    severus.components[-1].position=(severus.components[0].position[0],severus.components[0].position[1]-1)
                    severus.components=[severus.components.pop()]+severus.components
                    severus.direction=(0,-1)
                    
                if (snake_actions[np.argmax(nn_output)]=='DOWN' and severus.direction!=(0,-1)):
                    severus.components[-1].position=(severus.components[0].position[0],severus.components[0].position[1]+1)
                    severus.components=[severus.components.pop()]+severus.components
                    severus.direction=(0,1)
        
                    
                #If the snake finds food it will grow by lenght 1
                if severus.components[0].position==food.position:
                    #elongate snake with color of food
                    severus.components.append(SnakeComponent(grid.square_width,severus.tail.position,food.color,shape=food.shape))
                    
                    #update the score
                    header.score=severus.length()
                    
                    if header.score>=header.high_score:
                        header.high_score=header.score
                    
                    #generate new food at a location not on the snake
                    food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
                    while food_loc in severus.snake_space():
                        food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
                    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],grid=grid)
                    
                    #Increase snakes energy after eating food
                    severus.energy+=food_energy
                    
                    #Increase the snakes fitness for finding food
                    severus.fitness += reward_food
                    
                    #Pygame snakes cannot store more than 999 kilocalories, excess is not metabolized
                    if severus.energy>999:
                        severus.energy=999         
                else:
                    #If the snake bites its tail or wanders into the hunting zone the snake becomes injured
                    #note if snake does not move off of food in one frame it will register as biting its own tail
                    x,y=severus.components[0].position[0],severus.components[0].position[1]
                    if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows) or ((x,y) in severus.snake_space()[1:]):
                        #game over because of biting tail or out of bounds
                        severus.fitness += reward_hit_wall
                        game_on=False
                        
                    #If the snake tries to go out of bounds reset the head to the tail
                    #if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows):
                    #    severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)
                
                
                #The snake starved before finding food
                if severus.energy<=0:
                    game_on=False
                    
                    
                #If snake died of starvation, bit its tail or hit a wall
                if not game_on:
                    #print('snake injured at ('+str(x)+','+str(y)+')')
                    if header.high_score<=severus.length():
                        header.high_score=severus.length()
                    
                    #record how fit the snake was
                    fitness[index]=severus.fitness  
                    
                    #reset snake
                    severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)
                    
                    #reset food
                    food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
                    while food_loc in severus.snake_space():
                        food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
                    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],shape=severus.components[0].shape,grid=grid)

                    
                    #update score
                    header.score=severus.length()
                
                    #run=False: kill game | game_on=True: reset snake
                    #run=False
                    game_on=True
                    
                    #Break from while loop and continue with the next snake
                    break
    
    
                #REDRAW GAME WINDOW
                if watch:
                    redrawGameWindow()
                
        # =============================================================================
        # SELECT THE MOST FIT PARENTS TO SURVIVE AND BREED
        # =============================================================================
        print('Selecting the top snakes to breed...')
        #Agent[0]=(net[0],fitness[0])
        agents=selection(nets, fitness, survival_fraction)
        
        print('Agents:',str(len(agents)))
        
        # =============================================================================
        # PERFORM CROSSOVER TO MAKE CHILD NEURAL NETS FROM TOP PERFORMING PARENTS
        # =============================================================================
        print('Performing crossover...')
        nets=[agent[0] for agent in agents]
                
        nets.extend(crossover(agents, nn_shape, activation_functions,population))
        
        print('Nets:',str(len(nets)))
            

        # =============================================================================
        # RECORD STATISTICS    
        # =============================================================================
        history['best'].append(np.max(fitness))
        history['average'].append(np.mean(fitness))
        history['std'].append(np.std(fitness))
        history['run_time'].append(time.time()-t_start)
        
        reporter(history)
        print()
        
        
        print('Recording history...')
        #Save the ost recent copy of the history dictionary
        with open('./ga_snake_history/history.pkl','wb') as file:
            pickle.dump(history, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        
        # =============================================================================
        # SAVE THE BEST FIT PARENT TO MONITOR HOW THE POPULATION GREW FROM GENERATION TO GENERATION
        # =============================================================================
        print('Saving a copy of the best snake...')
        #Save a copy of the best neural network from each generation
        #nets[0].save_weights('./ga_snake_history/best/'+str(gen)+'_best')
        nets[0].save('./ga_snake_history/best/'+str(len(history['best'])+1)+'_best.h5')
        
        # =============================================================================
        # ADD RANDOM MUTATIONS
        # =============================================================================
        print('Adding mutations...\n')
        #Only mutate children, leave parents alone
        child_nets=mutate(nets[int(len(nets)*survival_fraction):], mutation_type=mutation_type, mutation_range=mutation_range, mutation_rate=mutation_rate, nn_shape=nn_shape, activation_functions=activation_functions)
        nets=nets[:int(len(nets)*survival_fraction)]+child_nets
        
        # =============================================================================
        # SAVE THE NEWLY CREATED POPULATION OF SNAKE NEURAL NETS AS A CHECKPOINT
        # =============================================================================
        print('Storing a backup copy of the top 500 snakes neural net weights...')
        #Save the most recent copy of the top 500 snakes
        save_count=0
        for net in nets:
            #net.save_weights('./ga_snake_history/checkpoint_weights/'+str(save_count)+'_weights')
            net.save('./ga_snake_history/checkpoint_weights/'+str(save_count)+'_weights.h5')
            save_count+=1
            if save_count==500:
                break
        print('Checkpoint process complete, OK to exit script.\n')
        
        # =============================================================================
        # IF A SATISFACTORY SNAKE EXISTS, BREAK (i.e. snake can reach a score of 200)
        # =============================================================================
        if max(fitness)>fitness_threshold:
            print('A super snake has been born.')
            break
        
        #reset snake population and fitness values for next round
        snakes = []
        fitness = [0]*population
        
        print('Repopulating snake bodies for next gen...')
        for i in range(population):
            snakes.append(Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy))


if __name__ == '__main__':
    from ga_tools import *
    from game_objects import *
    import settings_training
    settings=settings_training.settings
    
    print(settings)
    
    evalGenomes(**settings)
    
    pygame.quit()
    
    #main()