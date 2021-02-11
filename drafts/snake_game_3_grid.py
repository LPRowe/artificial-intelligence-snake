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
    def __init__(self,length,position,direction):
        self.length=length
        self.position=position
        self.direction=direction
        
        #keep an updated list of the components that make up the snake
        self.components=[]
        
class Component(object):
    '''each square that makes up the snake will be a component
    perhaps I will add an option for using different shapes'''
    def __init__(self,size,position):
        #width of each square
        self.size=size
        
        #location of each square (starting at the origin)
        self.position=(0,0)
        
        #this does nothing currently but may be useful later
        self.shape='square'
        
        
        
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
        
    
    def draw(self):
        #ADD LINES AND BOARDER
        x_line_spacing=(self.width-1)/self.rows
        y_line_spacing=(self.height-1)/self.columns
        
        #Vertical Lines
        for i in range(1,self.columns):
            pygame.draw.line(win,self.line_color,(self.x+i*x_line_spacing,self.y),(self.x+i*x_line_spacing,self.y+self.height),self.line_thickness)
        
        #Horizontal Lines
        for j in range(1,self.rows):
            pygame.draw.line(win,self.line_color,(self.x,self.y+j*y_line_spacing),(self.x+self.width,self.y+j*y_line_spacing),self.line_thickness)

        
        #Border
        pygame.draw.rect(win,self.border_color,(self.x,self.y,self.width,self.height),self.border_thickness)
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================
def redrawGameWindow():
    
    grid.draw()
    
    pygame.display.update()

# =============================================================================
# MAIN LOOP AND INITIAL CONDITIONS
# =============================================================================

def main():
    global game_on, grid, win
    
    #SET INITIAL CONDITIONS
    clock=pygame.time.Clock()
    width,height=500,500
    win=pygame.display.set_mode((width,height))
    
    #CREATE INITIAL OBJECTS
    #Square grid the same width as the window
    game_on=True
    grid=GridBoard(30,30,width,width,(0,0))
    

    run=True
    while run:
        
        pygame.time.delay(25)
        clock.tick(5)
        
        #get list of all events that happen i.e. keyboard, mouse, ...
        for event in pygame.event.get():
            #Check if the red X was clicked
            if event.type==pygame.QUIT:
                run=False
                
        #TRACK INPUTS FROM MOUSE/KEYBOARD HERE
        #{}
                
        
        #REDRAW GAME WINDOW
        redrawGameWindow()
    
    
    pygame.quit()
        
        
main()     
        
        
        
        
        
        
        
        