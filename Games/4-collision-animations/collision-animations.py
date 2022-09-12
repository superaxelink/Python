import pygame as py
import numpy as np
import time as tm
from pygame.locals import *
from random import random

py.mixer.pre_init()#44100, -16, 1, 512)
py.init()
py.mixer.init()
py.mixer.music.set_volume(0.2)
white = (255,255,255)
windowWidth = 500
windowHeight = 700 
screen = py.display.set_mode((windowWidth,windowHeight))
py.display.set_caption('Collision Animations')
explosions = []

class Explosion():
  def __init__(self,x,y):
    self.spriteWidth = 200
    self.spriteHeight = 179
    self.width = self.spriteWidth*0.7
    self.height = self.spriteHeight*0.7
    self.x = x
    self.y = y
    self.image = py.image.load("boom.png")
    self.frame = 0
    self.maxFrame = 4
    self.fps = 20
    self.timer = 0
    self.interval = 1/self.fps
    self.angle = np.random.random()*6.2
    self.sound = py.mixer.Sound("boom.wav") #AudioSegment.from_wav("boom.wav")
  def update(self,deltaTime):
    if(self.frame == 0): 
      py.mixer.Sound.stop(self.sound)
      py.mixer.Sound.play(self.sound)
      #_play_with_simpleaudio(self.sound)
    if(self.timer>self.interval):
      if(self.frame<self.maxFrame):
        self.frame +=1
        self.timer = 0
    else:
      self.timer += deltaTime
  def draw(self):
    crop = self.image.subsurface(self.spriteWidth * self.frame,0,self.spriteWidth,self.spriteHeight)
    py.transform.rotate(crop,self.angle)
    return py.transform.scale(crop,(self.width,self.height))
gameOn=True
deltaTime=0

def createAnimation(mouse):
  positionX = mouse[0] 
  positionY = mouse[1]  
  explosions.append(Explosion(positionX,positionY))

def animate(deltaTime,gameOn):
  while gameOn:
    t0 = tm.perf_counter()
    for event in py.event.get():
      if event.type == MOUSEBUTTONDOWN:
        createAnimation(py.mouse.get_pos())
      if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
          gameOn = False
      elif event.type == QUIT:
        gameOn = False
    #mouseState = py.mouse.get_pressed()[0] 
    screen.fill((0,0,0))
    i=0
    while i < len(explosions):
      print(len(explosions))
      explosions[i].update(deltaTime)
      screen.blit(explosions[i].draw(),(explosions[i].x - explosions[i].width*0.5,explosions[i].y- explosions[i].height*0.5))
      if (explosions[i].frame == explosions[i].maxFrame):
        explosions.pop(i)
        i -= 1 
        print(len(explosions))
      i += 1
    py.display.flip()
    deltaTime = tm.perf_counter() - t0

animate(deltaTime,gameOn)

