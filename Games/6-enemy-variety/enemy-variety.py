import pygame as py
import numpy as np
import time as tm
from pygame.locals import*

py.mixer.pre_init(44100, -16, 2, 512)
py.init()
py.mixer.init()
py.mixer.music.set_volume(0.2)
enemies = []
gameOn = True
white = (255,255,255)
windowWidth = 550
windowHeight	= 640
deltaTime = 0
screen = py.display.set_mode((windowWidth,windowHeight))
py.display.set_caption('Enemy variety')

class Game():
  def __init__(self,windowWidth,windowHeight):
    self.width = windowWidth
    self.height = windowHeight
    self.enemies = [] 
    self.enemyInterval = 0.5
    self.enemyTimer = 0
    self.enemyTypes = ['worm','ghost','spider']

  def update(self,deltaTime):
    self.enemies =  list(filter(lambda a : not a.markedForDeletion,self.enemies) )
    if(self.enemyTimer > self.enemyInterval):
      self.__addNewEnemy()
      self.enemyTimer = 0
    else:
      self.enemyTimer += deltaTime
    for object in self.enemies: 
      object.update(deltaTime)

  def draw(self,screen):
    screen.fill(white)
    for object in self.enemies: 
      object.draw(screen)
    py.display.flip()

  def checkEvent(self):
    for event in py.event.get():
      if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
          return False
      elif event.type == QUIT:
        return False
    return True

  def __addNewEnemy(self):
    randomEnemy = self.enemyTypes[np.floor(np.random.random()*len(self.enemyTypes)).astype(int)]
    if(randomEnemy == 'worm'): self.enemies.append(Worm(self))
    elif(randomEnemy == 'ghost'): self.enemies.append(Ghost(self))
    elif(randomEnemy == 'spider'): self.enemies.append(Spider(self))

class Enemy():
  def __init__(self,game):
    self.game = game
    self.markedForDeletion = False
    self.frameX = 0
    self.maxFrame = 5
    self.frameInterval = 0.2
    self.frameTimer = 0

  def update(self,deltaTime):
    self.x -= self.vx * deltaTime
    if(self.x < 0 -self.width): self.markedForDeletion = True
    if(self.frameTimer > self.frameInterval):
      if(self.frameX < self.maxFrame): self.frameX +=1
      else: self.frameX = 0
      self.frameTimer = 0
    else:
      self.frameTimer += deltaTime
  
  def draw(self,screen):
    crop = self.image.subsurface(self.spriteWidth * self.frameX,0,self.spriteWidth,self.spriteHeight)
    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x, self.y))
  
class Worm(Enemy):
  def __init__(self,game):
    super().__init__(game)
    self.spriteWidth = 229
    self.spriteHeight = 171
    self.width = self.spriteWidth * 0.5
    self.height = self.spriteHeight * 0.5
    self.x = self.game.width
    self.y = self.game.height - self.height
    self.image = py.image.load("enemy_worm.png").convert_alpha()
    self.vx = np.random.random() * 200 + 200

class Ghost(Enemy):
  def __init__(self,game):
    super().__init__(game)
    self.spriteWidth = 261
    self.spriteHeight = 209
    self.width = self.spriteWidth * 0.5
    self.height = self.spriteHeight * 0.5
    self.x = self.game.width
    self.y = np.random.random() * self.game.height * 0.4
    self.image = py.image.load("enemy_ghost.png")#.convert_alpha()#.set_alpha(100)
    self.vx = np.random.random() * 400 + 200
    self.angle = 0
    self.amplitude = np.random.random() * 0.5

  def update(self,deltaTime):
    super().update(deltaTime)
    self.y += self.amplitude*np.sin(self.angle)
    self.angle += 0.004

  def draw(self,screen):
    self.image.set_alpha(100)
    super().draw(screen)

class Spider(Enemy):
  def __init__(self,game):
    super().__init__(game)
    self.spriteWidth = 310
    self.spriteHeight = 175
    self.width = self.spriteWidth * 0.5
    self.height = self.spriteHeight * 0.5
    self.x = np.random.random() * self.game.width
    self.y = 0 - self.height
    self.image = py.image.load("enemy_spider.png").convert_alpha()
    self.vx = 0
    self.vy = np.random.random()*200 + 200
    self.maxLength = np.random.random() * self.game.height

  def update(self,deltaTime):
    super().update(deltaTime)
    if(self.y < 0 - self.height * 2): self.markedForDeletion = True
    self.y += self.vy * deltaTime
    if(self.y > self.maxLength): self.vy *= -1

  def draw(self,screen):
    py.draw.line(screen,(0,0,0),(self.x + self.width*0.5, 0),(self.x + self.width*0.5,self.y + 10))
    super().draw(screen)

game = Game(windowWidth,windowHeight)

def animate(deltaTime,gameOn):
  global screen
  while gameOn:
    t0 = tm.perf_counter()
    gameOn = game.checkEvent()
    game.update(deltaTime)
    game.draw(screen)
    deltaTime = tm.perf_counter() - t0

animate(0,gameOn)
