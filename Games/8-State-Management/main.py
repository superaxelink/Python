import pygame as py
import time as tm
from input import InputHandler 
from player import Player
from utils import drawStatusText
#import numpy as np

py.mixer.pre_init(44100, -16, 2, 512)
py.init()
py.mixer.init()
py.mixer.music.set_volume(0.2)
black = (0,0,0)
white = (255,255,255)
windowWidth = 1360
windowHeight	= 640
screen = py.display.set_mode((windowWidth,windowHeight))
py.display.set_caption('Side scroller')

def animate(t0):
  gameOn = True
  p1 = Player(windowWidth,windowHeight) 
  Input = InputHandler() 
  while gameOn:
    t1 = tm.perf_counter()
    deltaTime = t1 - t0
    t0 = t1
    gameOn = Input.checkEvent()
    screen.fill(white)
    p1.update(Input.lastkey)
    p1.draw(screen,deltaTime)
    drawStatusText(screen,Input,p1)
    py.display.flip()


animate(0)