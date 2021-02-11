# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:24:35 2020

@author: Logan Rowe
"""

from __future__ import print_function

import pygame
import numpy as np
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

pygame.init()

# =============================================================================
# LOAD SOUND EFFECTS AND MUSIC
# =============================================================================



class Snake(object):
    def __init__(self,direction,component,energy):
        
        #{'right':(1,0),'left':(-1,0),'up':(0,1),'down':(0,-1)}
        self.direction=direction
        
        #keep an updated list of the components that make up the snake
        self.components=[component]
        
        #Track the location just behind the tail for when the snake grows
        self.tail=self.components[-1]
        
        #Snake will die of hunger if it runs out of energy
        self.energy=energy
        
        
        
    def draw(self):
        
        square_width=grid.square_width
        square_height=grid.square_height
        
        #Draw the shape of each component at the components position
        for comp in self.components:
            if comp.shape=='square':
                x1,y1=grid.x+comp.position[0]*square_width,grid.y+(comp.position[1]-1)*square_height
                x2,y2=int(comp.size),int(comp.size)
                pygame.draw.rect(win,comp.color,(x1,y1,x2,y2),0)
            elif comp.shape=='circle':
                x1,y1=grid.x+int(square_width*comp.position[0]+0.5*comp.size),grid.y+int(square_height*comp.position[1]-0.5*comp.size)
                pygame.draw.circle(win,comp.color,(x1,y1),int(0.5*comp.size))
    
    
    def snake_space(self):
        '''Returns a list of positions [(0,1),(0,2),(0,3),(1,3)...] that the
        snake currently inhabits'''
        return [comp.position for comp in self.components]
    
    
    def length(self):
        return len(self.components)        
            
            
        
class SnakeComponent(object):
    '''each square that makes up the snake will be a component
    perhaps I will add an option for using different shapes'''
    def __init__(self,size,position,color,shape='square'):
        
        #width of each square
        self.size=size
        
        #location of each square (starting at the origin)
        self.position=position
        
        #Choose whether the snake is made up of circles or squares
        self.shape=shape
        
        self.color=color
        
        
class SnakeFood(object):
    '''Food will appear at a random location that is not on the snake
    whenever the previous food has been eaten'''
    def __init__(self,size,position,color,shape='circle'):
        
        #use position to draw food on the board
        self.position=position
        
        #use true position for collisions
        self.true_position=(self.position[0]+grid.x,self.position[1]+grid.y)
        
        self.color=color
        self.shape=shape
        self.size=size
    
    def draw(self):
        
        #Width and height of box on grid
        square_width=grid.square_width
        square_height=grid.square_height
        
        if self.shape=='square':
            x1,y1=grid.x+self.position[0]*square_width,grid.y+self.position[1]*square_height
            pygame.draw.rect(win,self.color,(x1,y1,self.size,self.size),0)
        elif self.shape=='circle':
            x1,y1=grid.x+int(square_width*self.position[0]+0.5*self.size),grid.y+int(square_height*self.position[1]-0.5*self.size)
            pygame.draw.circle(win,self.color,(x1,y1),int(0.5*self.size))
        
        
class GridBoard(object):
    '''create a grid for the snake to move around on'''
    def __init__(self,rows,columns,width,height,position):
        self.width=width
        self.height=height
        self.rows=rows
        self.columns=columns
        
        #Grid position on the window
        self.x,self.y=position
        
        #Set grid line properties
        self.line_thickness=1
        self.border_thickness=3
        self.line_color=(100,100,100)
        self.border_color=(255,255,255)
        
        #width of a given square
        self.square_width=(self.width)/self.rows
        self.square_height=(self.height)/self.columns
        
    
    def draw(self):
        #ADD LINES AND BOARDER
        x_line_spacing=(self.width-1)/self.rows
        y_line_spacing=(self.height-1)/self.columns
        
        #Vertical Lines
        for i in range(1,self.columns):
            pygame.draw.line(win,self.line_color,(self.x+i*self.square_width,self.y),(self.x+i*self.square_width,self.y+self.height),self.line_thickness)
        
        #Horizontal Lines
        for j in range(1,self.rows):
            pygame.draw.line(win,self.line_color,(self.x,self.y+j*self.square_height),(self.x+self.width,self.y+j*self.square_height),self.line_thickness)

        
        #Border
        pygame.draw.rect(win,self.border_color,(self.x,self.y,self.width,self.height),self.border_thickness)

class ScoreBoard(object):
    def __init__(self,score,shape,**properties):
        self.score=score
        self.shape=shape
        self.high_score=1
        
        self.font=pygame.font.SysFont('tahoma',int(0.5*self.shape[1]),bold=True)
        
        self.snake_icon_loc=(int(0.35*(win_width-snake_icon.get_size()[0])),int(0.5*(self.shape[1]-snake_icon.get_size()[1])))
        
        for key,val in properties.items():
            setattr(self, k, v)
    
    def draw(self):
        
        if self.score>=self.high_score:
            self.font_color=(0,200,0)
        else:
            self.font_color=(200,200,200)
            
        #add a snake icon
        win.blit(snake_icon,self.snake_icon_loc)

        #Add text for the score
        score_text=self.font.render('Score: '+str(int(self.score)),1,self.font_color)
        win.blit(score_text,(10,int(0.5*(self.shape[1]-score_text.get_size()[1]))))
        
        #Add text for high score
        high_score_text=self.font.render('High Score: '+str(int(self.high_score)),1,self.font_color)
        win.blit(high_score_text,(win_width-10-high_score_text.get_size()[0],int(0.5*(self.shape[1]-high_score_text.get_size()[1]))))
        
        #text color for snake energy (start green for healthy and traverse to red)
        healthy=350
        health=min(severus.energy,healthy)
        energy_color=(255*(1-health/healthy),255*health/healthy,0)
        
        #Add text for snakes current energy
        snake_energy_text=self.font.render(str(int(severus.energy)),1,energy_color)
        win.blit(snake_energy_text,(int(self.snake_icon_loc[0]+snake_icon.get_size()[0]+5),int(0.5*(self.shape[1]-snake_energy_text.get_size()[1]))))

# =============================================================================
# INPUT VALUES FOR NEURAL NETWORK ARE OUTPUT VALUES FROM WHAT SNAKE SEES
# =============================================================================

def snakeVision(snake,food):
    '''
    Takes the snake of interest and current food as inputs returns an output
    of 18 values that the snake sees and a list of the locations of obstructions.
    
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
             upright is also wall)=1 or (i.e. right is tail not touching wal 
             and up right is wall)=-1
    
    
    outputs=[x dist from snakes head to food,
             y dist from snakes head to food,
             dist to nearest obstruction to the right,
             dist to nearest obstruction to the up-right,
             dist to nearest obstruction to the up,
             dist to nearest obstruction to the up-left,
             dist to nearest obstruction to the left,
             dist to nearest obstruction to the down-left,
             dist to nearest obstruction to the down,
             dist to nearest obstruction to the downright,
             is connected right & right-up,
             is connected up & right-up,
             is connected up & left-up,
             is connected left & left-up,
             is connected left & down-left,
             is connected down & down-left,
             is connected down & down-right,
             is connected right & down-right,
             ]
    '''
    
    outputs=[]
    
    #Add Food location x distance and y distance (consistently using final position - initial position)
    outputs.append(food.position[0]-snake.components[0].position[0])
    outputs.append(food.position[1]-snake.components[0].position[1])    
    
    #locate obstructions (snake's tail or wall) in 8 directions 
    #[right, up-right, up, up-left, left, down-left, down, down-right]
    obstructions=[]
    
    #Positions currently inhabited by snake body
    snake_space=set(tuple(snake.snake_space()[1:]))
    
    #Position of the snakes head
    x_naught,y_naught=snake.components[0].position[0],severus.components[0].position[1]
    
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
    
    grid.draw()
    severus.draw()
    food.draw()
    header.draw()
    
    drawObstructions(obstructions)
    
    pygame.display.update()

# =============================================================================
# INITIAL CONDITIONS FOLLOWED BY RUN LOOP
# =============================================================================

def main():
    #objects
    global grid, win, severus, food, header
    
    #dimensions
    global grid_rows,grid_columns, win_width, win_height, food_energy
    
    #flags and values
    global colors, game_on, snake_icon, obstructions, snake_output
    
    
    #SET INITIAL CONDITIONS
    clock=pygame.time.Clock()
    win_width=500
    win_height=win_width+50
    win=pygame.display.set_mode((win_width,win_height))
    
    
    #Size of grid for snake to move on
    grid_columns,grid_rows=30,30
    
    
    #Range of colors to randomly choose from for snake food
    color_dict={'red':(255,0,0),
            'orange':(255,127,0),
            'yellow':(255,255,0),
            'green':(0,255,0),
            'blue':(0,0,255),
            'indigo':(75,0,130),
            'violet':(148,0,211)}
    colors=['red','orange','yellow','green','blue','indigo','violet']
    
    
    #Energy that each food contains
    food_energy=200
    
    
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
    header=ScoreBoard(severus.length(),(win_width,win_height-win_width))
    

    #Add food to the map in a location that the snake does not inhabit
    food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
    while food_loc in severus.snake_space():
        food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],shape=severus.components[0].shape)

    
    #run loop
    run=True
    while run:
        
        snake_output,obstructions=snakeVision(severus,food)
        
        #Set the speed the game runs at playing: (50,20) | training (0,comment out)
        pygame.time.delay(50)
        clock.tick(10)
        
        #Every time step, severus loses one energy [kcal]
        severus.energy-=1
        
        #get list of all events that happen i.e. keyboard, mouse, ...
        for event in pygame.event.get():
            #Check if the red X was clicked
            if event.type==pygame.QUIT:
                run=False
        
        #keep track of where the snakes tail is before movement incase it eats food
        severus.tail=severus.components[-1]
        
        keys=pygame.key.get_pressed()
        #TRACK INPUTS FROM MOUSE/KEYBOARD HERE
        if (keys[pygame.K_LEFT] and severus.direction!=(1,0)) or severus.direction==(-1,0):
            #Only allow a left turn if the snake is not going right
            
            #Update the snakes tail components position to be to the left of the snakes head This will create the illusion of the snake progressing forward
            severus.components[-1].position=(severus.components[0].position[0]-1,severus.components[0].position[1])
            #Move the tail component to the head position of the snake
            severus.components=[severus.components.pop()]+severus.components
            #Change the direction of the snake to left
            severus.direction=(-1,0)
            
            
        if (keys[pygame.K_RIGHT] and severus.direction!=(-1,0)) or severus.direction==(1,0):
            severus.components[-1].position=(severus.components[0].position[0]+1,severus.components[0].position[1])
            severus.components=[severus.components.pop()]+severus.components
            severus.direction=(1,0)
            
        if (keys[pygame.K_UP] and severus.direction!=(0,1)) or severus.direction==(0,-1):
            severus.components[-1].position=(severus.components[0].position[0],severus.components[0].position[1]-1)
            severus.components=[severus.components.pop()]+severus.components
            severus.direction=(0,-1)
            
        if (keys[pygame.K_DOWN] and severus.direction!=(0,-1)) or severus.direction==(0,1):
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
            food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)])
            
            #Increase snakes energy after eating food
            severus.energy+=food_energy
            
            #Pygame snakes cannot store more than 999 kilocalories, excess is not metabolized
            if severus.energy>999:
                severus.energy=999         
        else:
            #If the snake bites its tail or wanders into the hunting zone the snake becomes injured
            #note if snake does not move off of food in one frame it will register as biting its own tail
            x,y=severus.components[0].position[0],severus.components[0].position[1]
            if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows) or ((x,y) in severus.snake_space()[1:]):
                #game over because of biting tail or out of bounds
                game_on=False
                
            #If the snake tries to go out of bounds reset the head to the tail
            if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows):
                severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)
        
        
        #The snake starved before finding food
        if severus.energy<=0:
            game_on=False
            
            
        #If snake died of starvation, bit its tail or hit a wall
        if not game_on:
            print('snake injured at ('+str(x)+','+str(y)+')')
            if header.high_score<=severus.length():
                header.high_score=severus.length()
            
            severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)

            header.score=severus.length()
            
            #run=False: kill game | game_on=True: reset snake
            #run=False
            game_on=True
                
        
        #REDRAW GAME WINDOW
        redrawGameWindow()
    
    
    pygame.quit()
    

        
def evalGenomes(genomes, config):
    global win, gen
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    snakes = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy))
        ge.append(genome)
        
        '''
        for xi, xo in zip(xor_inputs, xor_outputs):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2
        '''
        
    
    
    
    
    
    

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(evalGenomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(evalGenomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    #run(config_path)
    
    main()
    
    
        
        
        
        
        
        
        
        