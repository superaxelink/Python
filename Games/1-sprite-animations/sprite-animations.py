import pygame
from pygame.locals import *
import time as tm

class Player():#pygame.sprite.Sprite):
  def __init__(self):
    #super(Player,self).__init__()
    #size of the square
    self.width = 575*0.4
    self.height = 523*0.4
    self.surf = pygame.Surface((self.width,self.height))
    #set color for the square
    self.color = (0,200,255)
    #to draw the square
    self.surf.fill(self.color)
    self.rect = self.surf.get_rect()
    #variables for the sprite
    self.spriteWidth = 575
    self.spriteHeight = 523
    self.frameX = 0
    self.frameY = 0
    self.maxFrame = 6
    #load the image for the sprite
    self.image = pygame.image.load(r'shadow_dog.png')
    self.timer = 0
    self.fps = 20 #fps wanted
    self.interval = 1/self.fps #target interval in seconds
    #crop for the sprite
    #self.sprite = pygame.transform.scale(self.image.subsurface((self.spriteWidth * self.frameX,self.spriteHeight * self.frameY,self.spriteWidth,self.spriteHeight)),(self.spriteWidth*0.4,self.spriteHeight*0.4))
  def update(self,deltaTime):
    if(self.timer > self.interval):
      if(self.frameX < self.maxFrame):
        self.frameX += 1
        self.timer = 0 
      else:
        self.frameX = 0
        self.timer = 0 
    else:
      self.timer += deltaTime
  def draw(self):
    return pygame.transform.scale(self.image.subsurface((self.spriteWidth * self.frameX,self.spriteHeight * self.frameY,self.spriteWidth,self.spriteHeight)),(self.spriteWidth*0.4,self.spriteHeight*0.4))
  
pygame.init()

white = (255,255,255)
windowWidth = 800
windowHeight = 600
screen = pygame.display.set_mode((windowWidth,windowHeight))

pygame.display.set_caption('Sprite-animations')
#create a square object

player = Player()
#sprite = pygame.Surface((575,523))
#sprite.fill(white)
#sprite.blit(image,(0,0),(0,0,575,523)) #lo mismo que subsurface

gameOn = True
lastTime = 0
deltaTime = 0
while gameOn:
  t0= tm.perf_counter()
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        gameOn = False
      if event.key == K_0:
        player.frameY = 0
        player.frameX = 0
        player.maxFrame = 6
      if event.key == K_1:
        player.frameY = 1
        player.frameX = 0
        player.maxFrame = 6
      if event.key == K_2:
        player.frameY = 2
        player.frameX = 0
        player.maxFrame = 6
      if event.key == K_3:
        player.frameY = 3
        player.frameX = 0
        player.maxFrame = 8
      if event.key == K_4:
        player.frameY = 4
        player.frameX = 0
        player.maxFrame = 10
      if event.key == K_5:
        player.frameY = 5
        player.frameX = 0
        player.maxFrame = 4
      if event.key == K_6:
        player.frameY = 6
        player.frameX = 0
        player.maxFrame = 6
      if event.key == K_7:
        player.frameY = 7
        player.frameX = 0
        player.maxFrame = 6
      if event.key == K_8:
        player.frameY = 8
        player.frameX = 0
        player.maxFrame = 10
      if event.key == K_9:
        player.frameY = 9
        player.frameX = 0
        player.maxFrame = 3
    elif event.type == QUIT:
      gameOn = False

  screen.fill(white)
  #screen.blit(player.surf,( (windowWidth - player.width)*0.5,(windowHeight - player.height)*0.5 ))
  screen.blit(player.draw(),( (windowWidth - player.width)*0.5,(windowHeight - player.height)*0.5 ))
  player.update(deltaTime)
  #screen.blit(sprite,(square1.x - square1.width*0.5,square1.y - square1.height*0.5)) #, (523,575, 200, 200))
  #screen.blit(surf.blit(), (square1.x - square1.width*0.5,square1.y - square1.height*0.5), (523,575, 200, 200))
  #screen.blit(image, (0,0))
  pygame.display.flip()
  deltaTime = tm.perf_counter() - t0

