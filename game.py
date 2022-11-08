import math
from random import randint
from numpy import quantile 
import pygame
from collections import deque
class Game:
    def __init__(self,screen) -> None:
        self.screen =screen
        self.apple=None
        self.snake=None
        self.grid=None
        self.vel=None
        self.is_over=True
        self.score=0.0
        self.level=3
    #Reset the game
    def reset(self):
        self.snake=deque([[14,13],[14,14],[14,15]],maxlen=3)
        self.apple=self._spawn_apple() 
        self.is_over=0.0
        self.change_direction(0)

    #Change direction of snake
    def change_direction(self,angle):
        xvel=math.cos(angle)
        yvel=math.sin(angle)
        self.vel=[int(xvel),int(yvel)]
         
    #Render the game
    def render(self):
        margin=2
        square_width=self.screen.get_width()//30
        square_height=self.screen.get_height()//30
        apple_row,apple_col=self.apple
        center=[apple_col*square_width +square_width/2, apple_row*square_height+ square_height//2]
        pygame.draw.circle(self.screen,[255,0,0],center,square_width/2-margin)
        for row,col in self.snake:
            rect=[col*square_width+margin,row*square_height+margin,square_width-margin,square_height-margin]
            pygame.draw.rect(self.screen,[255,255,0],rect,border_radius=2)
        font=pygame.font.SysFont("Verdana",10,True,True)
        text=font.render(f"Score : {self.score}",True,"red")
        self.screen.blit(text,[10,10])
        text=font.render(f"Best Score : {self.bs}",True,"red")
        self.screen.blit(text,[500,10])




    #Update state of game
    def update(self):
        self.check_collisions()
        head=self.snake[-1]
        new_location=[v1+v2 for v1,v2 in zip(head,self.vel)]
        self.snake.append(new_location)
        with open("best_score","r") as fic:
            self.bs=float(fic.read())
        self.level=int(self.score*0.75)+3
    def _spawn_apple(self):
        location=[randint(0,29),randint(0,29)]
        while location is self.snake:
            location =[randint(0,29),randint(0,29)]
        return location

    def check_collisions(self):
        headx,heady=self.snake[-1]
        if headx not in range(0,30) or heady not in range(0,29):
            self.is_over=True
        elif [headx,heady] in list(self.snake)[:-1]:
            self.is_over=True
        elif [headx,heady] ==self.apple:
            self.score+=1
            self.snake=deque(self.snake,self.snake.maxlen+1)
            self.apple=self._spawn_apple()
    def savebs(self):
        with open("best_score","r") as fic:
            bs=float(fic.read())
        if self.score> bs: 
            with open("best_score","w") as fic:
                fic.write(str(self.score))
    
        





