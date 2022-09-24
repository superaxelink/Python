from curses import window
import numpy as np
import pygame as pg
import time as tm
from UI import UserInterface
from Input import InputHandler
from player import Player
from background import Background
from enemies import FlyingEnemy, GroundEnemy, ClimbingEnemy

windowWidth = 500
windowHeight = 500
pg.init()
screen = pg.display.set_mode((windowWidth, windowHeight))
pg.display.set_caption("Endless Runner")

class Game():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.groundMargin = 80
    self.speed = 0
    self.maxSpeed = 2
    self.background = Background(self)
    self.player = Player(self)
    self.input = InputHandler(self)
    self.UI = UserInterface(self, self.width, self.height)
    self.enemies = []
    self.particles = []
    self.collisions = []
    self.maxParticles = 50
    self.enemyTimer = 0
    self.enemyInterval = 1
    self.debug = False
    self.score = 0
    self.fontColor = 'black'
    self.Time = 0
    self.maxTime = 10 #seconds
    self.winScore = 15
    self.gameOn = True
    self.gameOver = False
    self.player.currentState = self.player.states[0]
    self.player.currentState.enter()

  def update(self,deltaTime):
    self.gameOn, self.gameOver =self.input.checkEvent()   

    if(not self.gameOver):
      self.Time += deltaTime      
      self.background.update()
      self.player.update(self.input.keys, deltaTime)
      #handleEnemies
      if(self.enemyTimer > self.enemyInterval):
        self.addEnemy()
        self.enemyTimer = 0
      else:
        self.enemyTimer += deltaTime
    
      for enemy in self.enemies:
        enemy.update(deltaTime)
        if(enemy.markedForDeletion): 
          self.enemies = list(filter(lambda a : not a.markedForDeletion, self.enemies ))
      #handle particles
      for particle in self.particles:
        particle.update()
        if(particle.markedForDeletion): 
          self.particles = list(filter(lambda a : not a.markedForDeletion, self.particles ))#need to delete just the particle on certain index FIX
      if(len(self.particles) > self.maxParticles):
        #self.particles = self.particles.slice(0,self.maxParticles)#to remove when particles go over 50
        self.particles = self.particles[:50] #list(filter(self.maxParticles, self.particles ))
      #hanlde collision sprites
      for collision in self.collisions: 
        collision.update(deltaTime)
        if(collision.markedForDeletion): 
          self.collisions = list(filter(lambda a : not a.markedForDeletion, self.collisions ))#need to delete just the collision on certain index FIX 
    if(self.Time > self.maxTime): self.gameOver = True 
    if(self.score >= self.winScore ): self.gameOver = True  

  def draw(self,screen):
    self.background.draw(screen)
    self.player.draw(screen)
    for enemy in self.enemies:
      enemy.draw(screen)
    for particle in self.particles:
      particle.draw(screen,self.player.width,self.player.height)
    for collision in self.collisions:
      collision.draw(screen)
    self.UI.draw(screen,self.gameOver)

  def addEnemy(self):
    if(self.speed > 0 and np.random.random() < 0.5 ): self.enemies.append(GroundEnemy(self))
    elif(self.speed > 0): self.enemies.append(ClimbingEnemy(self))
    self.enemies.append(FlyingEnemy(self))

  def Reset(self):
    self.player.x = 0
    self.player.y = self.height - self.player.height - self.groundMargin
    self.enemies = []
    self.particles = []
    self.score = 0
    self.gameOver = not self.gameOver
    self.Time = 0
    for layer in self.background.backgroundLayers:
      layer.x = 0

game = Game(windowWidth, windowHeight)

def animate(t0, screen):
  while game.gameOn:
    t1 = tm.perf_counter()
    deltaTime = t1 - t0
    t0 = t1 
    game.update(deltaTime)
    game.draw(screen)
    #if(game.gameOver):
    pg.display.flip() 

animate(tm.perf_counter(),screen)