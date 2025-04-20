import pygame
from pygame.locals import *
import os
import random

pygame.init()
fps= 50
clock= pygame.time.Clock()
width= 700
height= 700
screen= pygame.display.set_mode((width, height))
TITLE= 'Flappy Bird'
pygame.display.set_caption(TITLE)

font= pygame.font.SysFont('Expo', 50) 
score= 0
pass_pipe= False
ground_scroll= 0
speed_scroll= 5
bg= pygame.image.load(os.path.join('images', 'fbbg.png'))
ground= pygame.image.load(os.path.join('images', 'ground.png'))
button_image= pygame.image.load(os.path.join('images', 'restart.png'))
pipe_gap= 150
pipe_frequency= 1500
game_over= False
fly= False
last_pipe= pygame.time.get_ticks()- pipe_frequency

def restart_game():
    pipe_group.empty()
    flappy.rect.x= 100
    flappy.rect.y= height//2
    score= 0
    return score

def draw_message(text, font, colour, x, y):
    image= font.render(text, True, colour) 
    screen.blit(image, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images= []
        self.index= 0
        self.counter= 0
        for i in range(3):
            img1= pygame.image.load(os.path.join('images', 'bird'+ str(i+ 1)+ '.png'))
            self.images.append(img1)
        self.image= self.images[self.index]
        self.rect= self.image.get_rect()
        self.rect.center= [x,y]
        self.v= 0
        self.click= False
    def update(self):
        if fly:
            self.v+= 0.5 #adding gravity
            if self.v> 8:
                self.v= 8
            if self.rect.bottom< 540:
                self.rect.y+= self.v
        if not game_over:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click= True
                self.v= -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.click= False
            self.counter+=1
            flapcooldown= 5
            if self.counter> flapcooldown:
                self.counter= 0
                self.index+= 1
                if self.index>len(self.images):
                    self.index= 0
            self.image= pygame.transform.rotate(self.images[self.index- 1], self.v* -2)
        else:
            self.image= pygame.transform.rotate(self.images[self.index- 1], -90)
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load(os.path.join('images', 'pipe.png'))
        self.rect= self.image.get_rect()
        # position 1 for pipe from top
        if pos == 1:
            self.image=pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft= [x, y- int(pipe_gap/2)]
        #position -1 for pipe
        if pos == -1:
            self.rect.topleft= [x, y+ int(pipe_gap/2)]
    def update(self):
        self.rect.x-=speed_scroll
        if self.rect.right< 0:
            self.kill()

class Button():
    def __init__(self, x, y, image ):
        self.image= image
        self.rect= self.image.get_rect()
        self.rect.center= (x,y)
    def draw(self):
        action= False
        pos= pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == [1]:
                action=True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

bird_group= pygame.sprite.Group()
flappy= Bird(width//2, height//2)        
bird_group.add(flappy)
pipe_group= pygame.sprite.Group()

button= Button(width//2, height//2, button_image)

running= True
while running:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    bird_group.update()
    screen.blit(ground, (ground_scroll, 540))
    draw_message(str(score), font, 'black', 20, 20)
    print(game_over, len(pipe_group))
    if len(pipe_group)> 0:
        if bird_group.sprites()[0].rect.left> pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right< pipe_group.sprites()[0].rect.right and pass_pipe == False:
            print('hello')
            pass_pipe= True
        if pass_pipe:
           if bird_group.sprites()[0].rect.left> pipe_group.sprites()[0].rect.right:
                score+= 1
                pass_pipe= False                
        
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top< 0:
        game_over= True
    if flappy.rect.bottom> 540:
        game_over= True
        fly= False
    if game_over == False and fly == True:
        time_now= pygame.time.get_ticks()
        if time_now- last_pipe> pipe_frequency:
            pipe_height= random.randint(-100,100)
            b_pipe= Pipe(width,height//2+pipe_height,-1)
            t_pipe= Pipe(width,height//2+pipe_height,1)
            pipe_group.add(b_pipe)
            pipe_group.add(t_pipe)
            last_pipe= time_now 
        ground_scroll-= speed_scroll
        if abs(ground_scroll)>35:
            ground_scroll= 0
        pipe_group.update()
    if game_over == True:
        # button.draw()
        if button.draw():
            
            game_over= False
            score= restart_game()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running= False
        if e.type == pygame.MOUSEBUTTONDOWN and fly == False and game_over == False:
            fly= True
    
    pygame.display.update()

pygame.quit()