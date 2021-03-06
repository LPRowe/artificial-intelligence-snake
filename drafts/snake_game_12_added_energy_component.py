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
# REDRAW GAME WINDOW     
# =============================================================================

def redrawGameWindow():
    
    pygame.draw.rect(win,(0,0,0),(0,0,win_width,win_height))
    
    grid.draw()
    severus.draw()
    food.draw()
    header.draw()
    
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
    global colors, game_on, snake_icon
    
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
        food_loc=tuple(np.random.randint(1,grid_columns),np.random.randint(1,grid_rows))

    food=SnakeFood(int(grid.square_width),food_loc,color_dict[np.random.choice(colors)],shape=severus.components[0].shape)



    run=True
    while run:
        
        #Set the speed the game runs at playing: (50,20) | training (0,comment out)
        pygame.time.delay(0)
        clock.tick(20)
        
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
            #note if snake does not move off of food in one frame it will register as biting its tail
            x,y=severus.components[0].position[0],severus.components[0].position[1]
            if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows) or ((x,y) in severus.snake_space()[1:]):
                #game over because of biting tail or out of bounds
                game_on=False
                
            #If the snake tries to go out of bounds reset the head to the tail
            if (x<0 or x>=grid_columns) or (y<1 or y>grid_rows):
                severus=Snake((1,0),SnakeComponent(int(grid.square_width),(int(0.5*grid_columns),int(0.5*grid_rows)),(0,255,0),shape='circle'),food_energy)
        
        if severus.energy<=0:
            #The snake starved before finding food
            game_on=False
            
        
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
        
if __name__=='__main__':
    main()
        
        
        
        
        
        
        
        