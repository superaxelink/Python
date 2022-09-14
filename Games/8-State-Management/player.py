import pygame as py
import numpy as np
from state import StandingLeft, StandingRight, SittingLeft, SittingRight, RunningLeft, RunningRight, JumpingLeft, JumpingRight, FallingLeft, FallingRight

class Player():
  def __init__(self,windowWidth, windowHeight):
    self.windowWidth = windowWidth 
    self.windowHeight = windowHeight #Height and width of the game window
    self.states = [StandingLeft(self),StandingRight(self), SittingLeft(self),
    SittingRight(self), RunningLeft(self), RunningRight(self), JumpingLeft(self), 
    JumpingRight(self), FallingLeft(self), FallingRight(self)] #states that the player will have
    self.currentState = self.states[1]#keep track of the current state
    self.image = py.image.load('dog.png')#the whole sprite image
    self.width = 200 
    self.height=181.83 #width and height of each sprite element
    self.x = self.windowWidth*0.5 - self.width*0.5
    self.y = self.windowHeight - self.height#positions in which each element of the sprite it's going to appear
    self.vy = 0
    self.weight = 0.029
    self.frameX = 0#to move horizontally in the sprite image
    self.frameY = 0#to move vertically in the sprite image
    self.maxFrame = 6
    self.speed = 0
    self.maxSpeed = 3
    self.fps = 30 #max fps per second
    self.frameTimer = 0 #timer
    self.frameInterval = 1/self.fps #number of miliseconds i want each frame to be displayed on the screen
    #before we switch to the next one

  def draw(self, screen, deltaTime):
    #update the frame
    if(self.frameTimer > self.frameInterval):
      if(self.frameX < self.maxFrame): self.frameX +=1
      else: self.frameX = 0
      self.frameTimer = 0
    else: self.frameTimer += deltaTime
    #crop and blit the image on the main surface
    crop = self.image.subsurface(self.width * self.frameX,self.height * self.frameY, self.width, self.height)
    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x, self.y))

  def update(self, input):
    self.currentState.handleInput(input)
    
    #horizontal movement
    self.x += self.speed
    if(self.x <= 0): self.x = 0 #if horizontal position is less or equal to 0 set position to zero
    elif(self.x >= self.windowWidth - self.width): self.x = self.windowWidth - self.width
    #if horizontal position is bigger than the right boundary minus the width of the image set position 
    #the right boundary minus the width of the image 

    #vertical movement
    self.y += self.vy
    if(not self.onGround()): self.vy += self.weight
    else: self.vy = 0
    if (self.y > self.windowHeight - self.height): self.y = self.windowHeight - self.height

  def setState(self,state): #to tell the state object towards which state 
    #we're going 
    self.currentState = self.states[state] #pass current state
    self.currentState.enter()

  def onGround(self):#check if player is standing on the ground
    return self.y >= self.windowHeight - self.height
  
