import pygame as pg
from pygame.locals import*

dict = {K_UP : "ArrowUp", K_DOWN : "ArrowDown", K_LEFT : "ArrowLeft", K_RIGHT : "ArrowRight", K_KP_ENTER : "Enter", K_RETURN:"Enter" ,K_SPACE: " "}

class InputHandler():
  def __init__(self,game):
    self.game = game
    self.keys = []

  def checkEvent(self):
    #print(self.keys)
    for event in pg.event.get():
      if event.type == KEYDOWN:
        if(event.key == K_BACKSPACE):
          return not self.game.gameOn, not self.game.gameOver #return for gameOn, gameOver. Both are boolean and empty the list
        if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT or event.key == K_KP_ENTER or K_RETURN or event.key == K_SPACE and self.keys.count(event.key) == 0):
          self.keys.append(dict[event.key])
        if(event.key == K_RETURN and self.game.gameOver):
          self.game.Reset()
      if event.type == KEYUP:
        if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT or event.key == K_KP_ENTER or event.key == K_SPACE or K_RETURN):
          self.keys.remove(dict[event.key])
      elif event.type == QUIT:
        return not self.game.gameOn, not self.game.gameOver
    return self.game.gameOn, self.game.gameOver