import pygame, math, sys

pygame.init()

class Config():

    mapsize = (2048,2048)
    width = 800
    height = 600
    screensize = (width,height)
    cornerpoint = [0,0]
    fps = 40
    scrollstepx = 0.5
    scrollstepy = 0.5



class View():

    def __init__(self):
        self.window = pygame.display.set_mode(Config.screensize)
        self.state = mainmenu

    def update(self):
        if self.state = mainmenu:
            mainmenu()

    def mainmenu()


class Eventhandler():
    

class Player(pygame.sprite.Sprite):

    def __init__(self):
        self.health = 100
        self.hunger = 100
        self.speed = 10
