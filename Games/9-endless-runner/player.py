import pygame as pg
from playerStates import Sitting, Running, Jumping, Falling, Rolling, Diving, Hit
from collisionAnimation import CollisionAnimation

class Player():
  def __init__(self,game):
    self.game = game
    self.width = 100
    self.height = 91.4
    self.x = 0
    self.y = self.game.height - self.height - self.game.groundMargin
    self.vy = 0
    self.weight = 0.1
    self.image = pg.image.load("assets/player.png").convert_alpha()
    self.frameX = 0
    self.frameY = 0
    self.maxFrame = 5
    self.fps = 20
    self.frameInterval = 1/self.fps
    self.frameTimer = 0
    self.speed = 0
    self.maxSpeed = 1.5
    self.rect = pg.Surface((self.width,self.height))
    self.states = [Sitting(self.game), Running(self.game), Jumping(self.game), Falling(self.game), Rolling(self.game), Diving(self.game), Hit(self.game)] 

  def update(self, input, deltaTime):
    self.checkCollision()
    self.currentState.handleInput(input)
    #horizontal movement
    self.x += self.speed
    #movement only available when not in state 6 (hit)
    if(input.count('ArrowRight') !=0 and self.currentState != self.states[6]): self.speed = self.maxSpeed
    elif(input.count('ArrowLeft') != 0 and self.currentState != self.states[6]): self.speed = -self.maxSpeed
    else: self.speed = 0
    #horizontal boundaries
    if (self.x<0): self.x = 0
    if (self.x > self.game.width - self.width): self.x = self.game.width - self.width
    #vertical movement
    self.y += self.vy
    if(not self.onGround()): self.vy += self.weight
    else: self.vy = 0
    #vertical boundaries
    if(self.y > self.game.height - self.height - self.game.groundMargin): self.y = self.game.height - self.height - self.game.groundMargin 
    #sprite animation
    if(self.frameTimer > self.frameInterval):
      self.frameTimer = 0
      if(self.frameX < self.maxFrame): self.frameX += 1
      else: self.frameX = 0
    else:
      self.frameTimer += deltaTime

  def draw(self, screen): 
    if(self.game.debug): #activate and deactive square visualization
      self.rect.set_alpha(100)
      self.rect.fill(self.color)
      screen.blit(self.rect,(self.x - self.width*0.5,self.y))
    crop = self.image.subsurface(self.width * self.frameX,self.height * self.frameY, self.width, self.height)
    screen.blit(pg.transform.scale(crop,(self.width,self.height)),(self.x, self.y))

  def onGround(self):
    return self.y >= self.game.height - self.height - self.game.groundMargin

  def setState(self, state, speed):
    self.currentState = self.states[state]
    self.game.speed = self.game.maxSpeed * speed
    self.currentState.enter()
    #console.log(this.currentState)

  def checkCollision(self):
    for enemy in self.game.enemies:
      if(enemy.x < self.x + self.width  and enemy.x + enemy.width > self.x and enemy.y < self.y + self.height and enemy.y + enemy.height > self.y):
        enemy.markedForDeletion = True
        self.game.collisions.append(CollisionAnimation(self.game, enemy.x + enemy.width * 0.5, enemy.y + enemy.height * 0.5))
        if(self.currentState == self.states[4] or self.currentState == self.states[5]):
          self.game.score +=1
        else:
          self.setState(6, 0)