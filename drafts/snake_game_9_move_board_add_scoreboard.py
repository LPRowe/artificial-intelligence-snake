# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:24:35 2020

@author: Logan Rowe
"""

import pygame
import numpy as np

pygame.init()

# =============================================================================
# LOAD GRAPHICS
# =============================================================================



# =============================================================================
# LOAD SOUND EFFECTS AND MUSIC
# =============================================================================



# =============================================================================
# SCALE SURFACES ACCORDING TO WINDOW SIZE
# =============================================================================



# =============================================================================
# ADD ALPHA CHANNELS TO IMAGES WITH OPAQUE BACKGROUNDS
# =============================================================================


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================



# =============================================================================
# CREATE OBJECTS TO INTERACT WITH
# =============================================================================


class Snake(object):
    def __init__(self,direction,component):
        
        #{'right':(1,0),'left':(-1,0),'up':(0,1),'down':(0,-1)}
        self.direction=direction
        
        #keep an updated list of the components that make up the snake
        self.components=[component]
        
        #Track the location just behind the tail for when the snake grows
        self.tail=self.components[-1]
        
        
        
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
    def __init__(self,**properties):
        for key,val in properties.items():
            setattr(self, k, v)
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    
    pygame.draw.rect(win,(0,0,0),(0,0,win_width,win_height))
    
    grid.draw()
    severus.draw()
    food.draw()
    
    pygame.display.update()

# =============================================================================
# MAIN LOOP AND INITIAL CONDITIONS
# =============================================================================

def main():
    global game_on, grid, win, severus, colors,food, grid_rows,grid_columns, win_width, win_height
    
    #SET INITIAL CONDITIONS
    clock=pygame.time.Clock()
    win_width,win_height=500,650
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
    
    
    #CREATE INITIAL OBJECTS
    #Square grid the same width as the window
    game_on=True
    grid=GridBoard(grid_columns,grid_rows,win_width,win_width,(0,win_height-win_width))
    
    severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'))
    
    #Add food to the map in a location that the snake does not inhabit
    food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
    while food_loc in severus.snake_space():
        food_loc=tuple(np.random.randint(1,grid_columns),np.random.randint(1,grid_rows))

    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],shape=severus.components[0].shape)

    run=True
    while run:
        
        pygame.time.delay(25)
        clock.tick(10)
        
        #get list of all events that happen i.e. keyboard, mouse, ...
        for event in pygame.event.get():
            #Check if the red X was clicked
            if event.type==pygame.QUIT:
                run=False
        
        #keep track of where the snakes tail is before movement incase it eats food
        severus.tail=severus.components[-1]
        
        keys=pygame.key.get_pressed()
        #TRACK INPUTS FROM MOUSE/KEYBOARD HERE
        if keys[pygame.K_LEFT] and severus.direction!=(1,0):
            #Only allow a left turn if the snake is not going right
            
            #Update the snakes tail components position to be to the left of the snakes head This will create the illusion of the snake progressing forward
            severus.components[-1].position=(severus.components[0].position[0]-1,severus.components[0].position[1])
            #Move the tail component to the head position of the snake
            severus.components=[severus.components.pop()]+severus.components
            #Change the direction of the snake to left
            severus.direction=(-1,0)
            
            
        if keys[pygame.K_RIGHT] and severus.direction!=(-1,0):
            severus.components[-1].position=(severus.components[0].position[0]+1,severus.components[0].position[1])
            severus.components=[severus.components.pop()]+severus.components
            severus.direction=(1,0)
            
        if keys[pygame.K_UP] and severus.direction!=(0,1):
            severus.components[-1].position=(severus.components[0].position[0],severus.components[0].position[1]-1)
            severus.components=[severus.components.pop()]+severus.components
            severus.direction=(0,-1)
            
        if keys[pygame.K_DOWN] and severus.direction!=(0,-1):
            severus.components[-1].position=(severus.components[0].position[0],severus.components[0].position[1]+1)
            severus.components=[severus.components.pop()]+severus.components
            severus.direction=(0,1)

            
        #If the snake finds food it will grow by lenght 1
        if severus.components[0].position==food.position:
            #elongate snake with color of food
            severus.components.append(SnakeComponent(grid.square_width,severus.tail.position,food.color,shape=food.shape))
            
            #generate new food at a location not on the snake
            food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
            while food_loc in severus.snake_space():
                food_loc=tuple((np.random.randint(1,grid_columns),np.random.randint(1,grid_rows)))
            food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)])
        else:
            #If the snake bites its tail or wanders into the hunting zone the snake becomes injured
            #note if snake does not move off of food in one frame it will register as biting its tail
            x,y=severus.components[0].position[0],severus.components[0].position[1]
            if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows) or ((x,y) in severus.snake_space()[1:]):
                #game over because of biting tail or out of bounds
                game_on=False
        
        if not game_on:
            print('snake injured at ('+str(x)+','+str(y)+')')
            game_on=True
                
        
        #REDRAW GAME WINDOW
        redrawGameWindow()
    
    
    pygame.quit()
        
        
main()
        
        
        
        
        
        
        
        