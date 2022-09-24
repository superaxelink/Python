import numpy as np
import pygame as pg

class Particle():
  def __init__(self, game):
    self.game = game
    self.markedForDeletion = False

  def update(self):
    self.x -= self.speedX + self.game.speed
    self.y -= self.speedY
    self.size *= 0.95 #each particle will decrease for 5% on every frame. This controls how long is the particle trail
    #print(self.size)
    if(self.size < 0.5): self.markedForDeletion = True

class Dust(Particle):
  def __init__(self, game, x, y):
    super().__init__(game)
    self.size = np.random.random() * 10 + 10
    self.x = x
    self.y = y
    self.speedX = np.random.random()
    self.speedY = np.random.random()
    self.alpha = np.random.random()*80
    self.color = (0, 0, 0) 

  def draw(self, screen, playerWidth, playerHeight):
    rect = pg.Surface((2*self.size,2*self.size),pg.SRCALPHA)
    pg.draw.circle(rect,self.color + (self.alpha,),(self.size,self.size),self.size)
    screen.blit(rect,(self.x,self.y-self.size))
    #pg.draw.circle(screen,self.color,(self.x,self.y),self.size)

class Splash(Particle):
  def __init__(self, game, x, y):
    super().__init__(game)
    self.size = np.random.random() * 100 + 100
    self.x = x - self.size * 0.4
    self.y = y - self.size * 0.5
    self.speedX = np.random.random() * 6 - 3
    self.speedY = np.random.random() * 2 + 2
    self.gravity = 0
    self.image = pg.image.load('assets/fire.png').convert_alpha()

  def update(self):
    super().update()
    self.gravity += 0.1
    self.y += self.gravity

  def draw(self, screen, playerWidth, playerHeight):
    screen.blit(pg.transform.scale(self.image,(self.size,self.size)),(self.x, self.y))

class Fire(Particle):
  def __init__(self, game, x, y):
    super().__init__(game)
    self.image = pg.image.load('assets/fire.png').convert_alpha()
    self.size = np.random.random() * 100 + 50 #in pixels
    self.x = x
    self.y = y
    self.speedX = 1
    self.speedY = 1
    self.angle = 0 #to rotate fire
    self.va = np.random.random() * 0.2 - 0.1 #velocity of angle

  def update(self):
    super().update()
    self.angle += self.va
    self.x += np.sin(self.angle * 10)
  
  def draw(self,screen, playerWidth, playerHeight):
    crop = pg.transform.rotate(self.image, self.angle)
    screen.blit(pg.transform.scale(crop,(self.size,self.size)),(self.x - self.size*0.5, self.y - self.size*0.5))

    # - playerWidth*0.5
    #- playerHeight*0.5