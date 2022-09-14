import pygame as py
from pygame.locals import*

class InputHandler():
  def __init__(self):
    self.lastkey = ''

  def checkEvent(self):
    for event in py.event.get():
      if event.type == KEYDOWN:
        if(event.key == K_BACKSPACE):
          return False
        if(event.key == K_UP):
          self.lastkey = 'PRESS up'
        elif(event.key == K_DOWN):
          self.lastkey = 'PRESS down'
        elif(event.key == K_LEFT):
          self.lastkey = 'PRESS left'
        elif(event.key == K_RIGHT):
          self.lastkey = 'PRESS right'
      elif event.type == KEYUP:
        if(event.key == K_UP):
          self.lastkey = 'RELEASE up'
        elif(event.key == K_DOWN):
          self.lastkey = 'RELEASE down'
        elif(event.key == K_LEFT):
          self.lastkey = 'RELEASE left'
        elif(event.key == K_RIGHT):
          self.lastkey = 'RELEASE right'
      elif event.type == QUIT:
        return False #return for gameOn
    return True #return for gameOn
