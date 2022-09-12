from random import random
import pygame
import numpy as np
from pygame.locals import *
import time as tm

pygame.init()
white = (255,255,255)
windowWidth = 500
windowHeight = 1000
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Enemy movement pattern')

numberOfEnemies = 10

class Enemy():
  def __init__(self,image,spriteWidth,spriteHeight,maxFrame,angle, angleSpeed, curve, mode):
    #source image and data about it
    self.image = image
    self.frame = 0
    self.maxFrame = maxFrame
    self.spriteWidth = spriteWidth
    self.spriteHeight = spriteHeight
    self.width = self.spriteWidth/2.5
    self.height = self.spriteHeight/2.5
    #speed of movement
    self.speed = np.random.random()*4 +1
    self.x = np.random.random() * (windowWidth - self.width)
    self.y = np.random.random() * (windowHeight - self.height)
    self.flapSpeed = np.floor(np.random.random() * 3 + 1)
    #to control animation speed
    self.timer = 0
    self.fps = 20 #fps wanted
    self.interval = 1/self.fps #target interval in seconds
    #angular movement
    self.angle = angle # Indicates where in the senoidal movement the position begins.
    self.angleSpeed = angleSpeed #randomize movement of each enemy
    self.curve = curve #changes amplitude of senoidal movement
    self.mode = mode
    self.newX = np.random.random() * windowWidth
    self.newY = np.random.random() * windowHeight
    self.counter = 0 #counter to add random speeds with the model = 3 enemies

  def update(self,deltaTime,updatex,updatey):
    if(self.timer>self.interval):
      if(self.mode ==0 or self.mode==1):
        self.x += updatex
        self.y += updatey
      elif(self.mode == 2):
        self.x = updatex
        self.y = updatey
      elif(self.mode == 3):
        if(self.counter % self.curve == 0):
          self.newX = np.random.random() * (windowWidth - self.width)
          self.newY = np.random.random() * (windowHeight - self.height)
        dx = self.x - self.newX
        dy = self.y - self.newY
        self.x -= dx/70
        self.y -= dy/70
        self.y += np.random.random()*10 - 5 
        self.counter += 1
      if(self.frame < self.maxFrame):
        self.frame += 1
        self.timer = 0
      else:
        self.frame = 0
        self.timer = 0
      self.angle += self.angleSpeed
      if(self.x + self.width < 0):
        self.x = windowWidth
    else:
      self.timer += deltaTime
  def draw(self):
    return pygame.transform.scale(self.image.subsurface((self.spriteWidth * self.frame, 0 ,self.spriteWidth,self.spriteHeight)),(self.spriteWidth*0.4,self.spriteHeight*0.4))

bats1 = []
bats2 = []
ghosts = []
saws =[]

for i in range(int(numberOfEnemies*2.5)):
  bats1.append(Enemy(pygame.image.load("enemy1.png").convert_alpha(),293,155,4,0,0,0,0))
  bats2.append(Enemy(pygame.image.load("enemy2.png").convert_alpha(),266,188,4,0,np.random.random()*0.2,np.random.random()*10,1))
  ghosts.append(Enemy(pygame.image.load("enemy3.png").convert_alpha(),218,177,4,np.random.random()*500,np.random.random()*0.5 + 0.5,np.random.random()*200 + 50, 2))
  saws.append(Enemy(pygame.image.load("enemy4.png").convert_alpha(),213,212,7,0,0,np.floor(np.random.random()*200 + 50),3))
gameOn = True
deltaTime = 0
def animate(deltaTime,gameOn):
  while gameOn:
    t0= tm.perf_counter()
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
          gameOn = False
      elif event.type == QUIT:
        gameOn = False

    screen.fill(white)
    for bat in bats1:
      screen.blit(bat.draw(),(bat.x,bat.y))
      bat.update(deltaTime,np.random.random()*15 - 7.5,np.random.random()*10 - 5)
    for bat in bats2:
      screen.blit(bat.draw(),(bat.x,bat.y))
      bat.update(deltaTime,-bat.speed, bat.curve * np.sin(bat.angle) + np.random.random()*10 -5)
    for ghost in ghosts:
      screen.blit(ghost.draw(),(ghost.x,ghost.y))
      ghost.update(deltaTime, ghost.curve * np.cos(ghost.angle * np.pi/90) + (windowWidth*0.5 - ghost.width*0.5), ghost.curve * np.sin(ghost.angle * np.pi/270) + (windowWidth*0.5 - ghost.height*0.5+ np.random.random()*10 -5))
    for saw in saws:
      screen.blit(saw.draw(),(saw.x,saw.y))
      saw.update(deltaTime, 0, 0)

    pygame.display.flip()
    deltaTime = tm.perf_counter() - t0
animate(deltaTime,gameOn)


