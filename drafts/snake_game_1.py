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
        
        
        
class board(object):
    '''create a grid for the snake to move around on'''
    def __init__(self,rows,columns,width):
        pass
        
# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    pass

# =============================================================================
# MAIN LOOP
# =============================================================================

def main():
    width,height=500,500
    
    clock=pygame.time.Clock()
    
    run=True
    while run:
        
        pygame.time.delay(25)
        clock.tick(5)