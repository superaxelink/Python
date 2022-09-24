import pygame as pg
import numpy as np

class Enemy():
  def __init__(self):
    self.frameX = 0
    self.frameY = 0
    self.fps = 10
    self.frameInterval = 1/self.fps
    self.frameTimer = 0
    self.markedForDeletion = False

  def update(self,deltaTime):
    #movement
    self.x -= self.speedX + self.game.speed 
    self.y += self.speedY
    if(self.frameTimer > self.frameInterval):
      self.frameTimer = 0
      if(self.frameX < self.maxFrame): self.frameX += 1
      else: self.frameX = 0
    else:
      self.frameTimer += deltaTime  

    #check if off screen
    if (self.x + self.width < 0): self.markedForDeletion = True

  def draw(self,screen):
    if(self.game.debug): #activate and deactive square visualization
      self.rect.set_alpha(100)
      self.rect.fill(self.color)
      screen.blit(self.rect,(self.x - self.width*0.5,self.y))
    crop = self.image.subsurface(self.width * self.frameX,self.height * self.frameY, self.width, self.height)
    screen.blit(pg.transform.scale(crop,(self.width,self.height)),(self.x, self.y))


class FlyingEnemy(Enemy):
  def __init__(self,game):
    super().__init__()
    self.game = game
    self.width = 60
    self.height = 44
    self.x = self.game.width + np.random.random() *self.game.width * 0.5
    self.y = np.random.random() * self.game.height * 0.5
    self.speedX = np.random.random() + 1
    self.speedY = 0
    self.maxFrame = 5
    self.image = pg.image.load('assets/enemy_fly.png').convert_alpha()
    self.angle = 0 
    self.va = np.random.random() * 0.1 + 0.1
    self.rect = pg.Surface((self.width,self.height))
  
  def update(self,deltaTime):
    super().update(deltaTime)
    self.angle += self.va
    self.y += np.sin(self.angle)

  def draw(self,screen):
    super().draw(screen)

class GroundEnemy(Enemy):
  def __init__(self,game):
    super().__init__()
    self.game = game
    self.width = 60
    self.height = 87
    self.x = self.game.width
    self.y = self.game.height - self.height - self.game.groundMargin
    self.image = pg.image.load('assets/enemy_plant.png').convert_alpha()
    self.speedX = 0
    self.speedY = 0
    self.maxFrame = 1
    self.rect = pg.Surface((self.width,self.height))

  def update(self,deltaTime):
    super().update(deltaTime)

  def draw(self, screen):
    super().draw(screen)

class ClimbingEnemy(Enemy):
  def __init__(self,game):
    super().__init__()
    self.game = game
    self.width = 120
    self.height = 144
    self.x = self.game.width
    self.y = np.random.random() * self.game.height * 0.5
    self.image = pg.image.load('assets/enemy_spider_big.png').convert_alpha()
    self.speedX = 0
    self.speedY = 1 if np.random.random() > 0.5 else -1
    self.maxFrame = 5
    self.rect = pg.Surface((self.width,self.height))

  def update(self,deltaTime):
    super().update(deltaTime)
    if(self.y > self.game.height - self.height - self.game.groundMargin): self.speedY *= -1
    if(self.y < -self.height): self.markedForDeletion = True

  def draw(self,screen):
    super().draw(screen)
    pg.draw.line(screen,(0,0,0),(self.x + self.width*0.5, 0),(self.x + self.width*0.5,self.y + 10))