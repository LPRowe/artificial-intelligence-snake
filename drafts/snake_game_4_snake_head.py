# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:24:35 2020

@author: Logan Rowe
"""

import pygame
import numpy

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
        
        #length and position are initially not set
        self.length=-1
        self.possition=-1
        
    def draw(self):
        
        square_width=grid.square_width
        square_height=grid.square_height
        
        #Draw the shape of each component at the components position
        for comp in self.components:
            if comp.shape=='square':
                x1,y1=comp.position[0]*square_width,comp.position[1]*square_height
                x2,y2=int(comp.size),int(comp.size)
                pygame.draw.rect(win,comp.color,(x1,y1,x2,y2),0)
            elif comp.shape=='circle':
                x1,y1=int(square_width*comp.position[0]+0.5*comp.size),int(square_height*comp.position[1]-0.5*comp.size)
                pygame.draw.circle(win,comp.color,(x1,y1),int(0.5*comp.size))
        
class SnakeComponent(object):
    '''each square that makes up the snake will be a component
    perhaps I will add an option for using different shapes'''
    def __init__(self,size,position,color,shape='square'):
        #width of each square
        self.size=size
        
        #location of each square (starting at the origin)
        self.position=position
        
        #this does nothing currently but may be useful later
        self.shape=shape
        
        self.color=color
        
        
        
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
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    
    grid.draw()
    severus.draw()
    
    pygame.display.update()

# =============================================================================
# MAIN LOOP AND INITIAL CONDITIONS
# =============================================================================

def main():
    global game_on, grid, win, severus
    
    #SET INITIAL CONDITIONS
    clock=pygame.time.Clock()
    width,height=500,500
    win=pygame.display.set_mode((width,height))
    
    grid_columns,grid_rows=30,30
    
    #CREATE INITIAL OBJECTS
    #Square grid the same width as the window
    game_on=True
    grid=GridBoard(grid_columns,grid_rows,width,width,(0,0))
    
    severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'))
    

    run=True
    while run:
        
        pygame.time.delay(25)
        clock.tick(5)
        
        #get list of all events that happen i.e. keyboard, mouse, ...
        for event in pygame.event.get():
            #Check if the red X was clicked
            if event.type==pygame.QUIT:
                run=False
        
        keys=pygame.keys.get_pressed()
        #TRACK INPUTS FROM MOUSE/KEYBOARD HERE
        #{}
                
        
        #REDRAW GAME WINDOW
        redrawGameWindow()
    
    
    pygame.quit()
        
        
main()     
        
        
        
        
        
        
        
        