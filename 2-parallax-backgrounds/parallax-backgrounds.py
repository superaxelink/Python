import pygame
from pygame.locals import *
import time as tm

pygame.init()

white = (255,255,255)
windowWidth = 800
windowHeight = 700
gameSpeed = 20
screen = pygame.display.set_mode((windowWidth,windowHeight))

pygame.display.set_caption('Sprite-animations')

backgroundLayer1 = pygame.image.load("layer-1.png").convert_alpha()
backgroundLayer2 = pygame.image.load("layer-2.png").convert_alpha()
backgroundLayer3 = pygame.image.load("layer-3.png").convert_alpha()
backgroundLayer4 = pygame.image.load("layer-4.png").convert_alpha()
backgroundLayer5 = pygame.image.load("layer-5.png").convert_alpha()

class Layer():
  def __init__(self,image,speedModifier):
    self.x = 0
    self.y = 0
    self.width = 2400
    self.height = 700
    self.image = image
    self.speedModifier = speedModifier
    self.speed = gameSpeed * self.speedModifier
  def update(self):
    self.speed = gameSpeed * self.speedModifier
    if(self.x <= -self.width):
      self.x=0; 
    self.x = self.x - self.speed
  def draw(self):
    return pygame.transform.scale(self.image,(self.width,self.height))
    #pygame.transform.scale(self.image,(self.width,self.height))

layer1 = Layer(backgroundLayer1,0.2)
layer2 = Layer(backgroundLayer2,0.4)
layer3 = Layer(backgroundLayer3,0.6)
layer4 = Layer(backgroundLayer4,0.8)
layer5 = Layer(backgroundLayer5,1)


gameObjects = [layer1,layer2, layer3, layer4, layer5]

gameOn = True
lastTime = 0
deltaTime = 0
while gameOn:
  #t0= tm.perf_counter()
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        gameOn = False
    elif event.type == QUIT:
      gameOn = False

  screen.fill(white)
  for layer in gameObjects:
    screen.blit(layer.draw(),(layer.x,layer.y))
    screen.blit(layer.draw(),(layer.x + layer.width,layer.y))
    layer.update()
  pygame.display.flip()
  #deltaTime = tm.perf_counter() - t0
  #print(deltaTime)

