#import the pygame module
import pygame
from pygame.locals import *

# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects

class Square(pygame.sprite.Sprite):
  def __init__(self):
    super(Square, self).__init__()

    #Define the dimension of the surface
    #Here we're making squares of side 25px
    self.surf = pygame.Surface((25,25))

    #Color of the surfing
    self.surf.fill((0,200,255))
    self.rect = self.surf.get_rect()

#initialization of pygame
pygame.init()

#define the dimensions of the screen project
screen = pygame.display.set_mode((800,600))

#Create the square objects
square1 = Square()
square2 = Square()
square3 = Square()
square4 = Square()

#variable to keep our game loop running

gameOn = True

#Our game loop
while gameOn:
  #for loop through the event queue
  for event in pygame.event.get():
    #check for keydown event
    if event.type == KEYDOWN:
      #If the backspace has been pressed set
      #running to false to exit the main loop
      if event.key == K_BACKSPACE:
        gameOn = False
    #check for quit event
    elif event.type == QUIT:
      gameOn = False
  #Define where the squares will appear on the screen
  #Use blit to draw them on the screen surface
  screen.blit(square1.surf,(40,40))
  screen.blit(square2.surf,(40,530))
  screen.blit(square3.surf,(730,40))
  screen.blit(square4.surf,(730,530))

  #update the display using flip
  pygame.display.flip()