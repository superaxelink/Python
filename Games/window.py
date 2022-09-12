import pygame

#Define background color
#Using rgb color coding
background_color = (234,212,252)

#define dimensions of screen object
screen = pygame.display.set_mode((300, 300))

#set the caption of the screen
pygame.display.set_caption('Axl window')

#Fill the background color to the screen
screen.fill(background_color)

#update the display using flip
pygame.display.flip()

#variable to keep our game loop running
running = True

#game loop
while running:
  #for loop through the event queue
  for event in pygame.event.get():
    #check for quit event
    if event.type == pygame.QUIT:
      running = False
