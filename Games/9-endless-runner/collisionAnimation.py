import pygame as pg
import numpy as np

class CollisionAnimation():
  def __init__(self, game, x, y):
    self.game = game
    self.image = pg.image.load('assets/boom.png').convert_alpha()
    self.spriteWidth = 100
    self.spriteHeight = 90
    self.sizeModifier = np.random.random() + 0.5
    self.width = self.spriteWidth * self.sizeModifier
    self.height = self.spriteHeight * self.sizeModifier
    self.x = x - self.width * 0.5
    self.y = y - self.height * 0.5
    self.frameX = 0
    self.frameY = 0
    self.maxFrame = 4
    self.markedForDeletion = False
    self.fps = np.random.random() * 10 + 5
    self.frameInterval = 1/self.fps
    self.frameTimer = 0

  def draw(self, screen):
    crop = self.image.subsurface(self.spriteWidth * self.frameX,self.spriteHeight * self.frameY, self.spriteWidth, self.spriteHeight)
    screen.blit(pg.transform.scale(crop,(self.width,self.height)),(self.x, self.y))

  def update(self,deltaTime):
    self.x -= self.game.speed
    if(self.frameTimer > self.frameInterval):
      self.frameX += 1
      self.frameTimer = 0
    else:
      self.frameTimer += deltaTime
    if(self.frameX > self.maxFrame): self.markedForDeletion = True