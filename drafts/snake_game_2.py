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

class snake(object):
    def __init__(self,length,position,direction):
        self.length=length
        self.position=position
        self.direction=direction
        
        #keep an updated list of the components that make up the snake
        self.components=[]
        
class component(object):
    '''each square that makes up the snake will be a component
    perhaps I will add an option for using different shapes'''
    def __init__(self,size,position):
        #width of each square
        self.size=size
        
        #location of each square (starting at the origin)
        self.position=(0,0)
        
        #this does nothing currently but may be useful later
        self.shape='square'
        
        
        
class grid(object):
    '''create a grid for the snake to move around on'''
    def __init__(self,rows,columns,width,height):
        self.width=width
        self.height=height
        self.rows=rows
        self.columns=columns
    
    def draw(self):
        pass
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    pass

# =============================================================================
# MAIN LOOP AND INITIAL CONDITIONS
# =============================================================================

def main():
    #SET INITIAL CONDITIONS
    clock=pygame.time.Clock()
    width,height=500,500
    win=pygame.display.set_mode((width,height))

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
        
        
        
        
if __name__=='__main__':
    main()     
        
        
        
        
        
        
        
        