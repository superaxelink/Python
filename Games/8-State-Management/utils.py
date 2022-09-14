import pygame as py
def drawStatusText(screen,input,player):
  font = py.font.SysFont(None,30)
  img1 = font.render('Last input: ' + input.lastkey,True, (0,0,0))
  img2 = font.render('Active state: ' + player.currentState.state,True, (0,0,0))
  screen.blit(img1,(20,50))
  screen.blit(img2,(20,90))

