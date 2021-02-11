# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:54:36 2020

@author: rowe1

Contains all of the objects used within the snake game

- snake and the components that it is composed of
- food
- board that snake moves around on
- score board (header) that displays high score, current score, icon and snake life

"""


import pygame
import numpy as np

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
        
        #Rating of how well the snake performed during its life ~ used for genetic algorithm breeding
        self.fitness=0
        
        
        
    def draw(self,win,grid):
        
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
    def __init__(self,size,position,color,shape='circle',grid=None):
        
        #use position to draw food on the board
        self.position=position
        
        #use true position for collisions
        self.true_position=(self.position[0]+grid.x,self.position[1]+grid.y)
        
        self.color=color
        self.shape=shape
        self.size=size
    
    def draw(self,win,grid):
        
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
        
    
    def draw(self,win):
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
    def __init__(self,score,shape,win_width,snake_icon):
        self.score=score
        self.shape=shape
        self.high_score=1
        
        self.font=pygame.font.SysFont('tahoma',int(0.5*self.shape[1]),bold=True)
        
        self.snake_icon_loc=(int(0.35*(win_width-snake_icon.get_size()[0])),int(0.5*(self.shape[1]-snake_icon.get_size()[1])))
        

    
    def draw(self,win,win_width,energy,snake_icon):
        
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
        health=min(energy,healthy)
        energy_color=(255*(1-health/healthy),255*health/healthy,0)
        
        #Add text for snakes current energy
        snake_energy_text=self.font.render(str(int(energy)),1,energy_color)
        win.blit(snake_energy_text,(int(self.snake_icon_loc[0]+snake_icon.get_size()[0]+5),int(0.5*(self.shape[1]-snake_energy_text.get_size()[1]))))