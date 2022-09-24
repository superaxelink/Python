import pygame as pg

class UserInterface():
  def __init__(self, game, windowWidth, windowHeight):
    self.game = game
    self.fontSize = 30
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.fontFamily = 'Helvetica'

  def draw(self, screen, gameOver):
    font = pg.font.SysFont(None,24)
    img1 = font.render('Score: ' + str(self.game.score),True, (0,0,0))
    img2 = font.render('Score: ' + str(self.game.score),True, (255, 255, 255))
    img3 = font.render('Time: ' + '{0:.1f}'.format(self.game.Time),True, (0,0,0))
    img4 = font.render('Time: ' + '{0:.1f}'.format(self.game.Time),True, (255, 255, 255))
    screen.blit(img1,(50,55))
    screen.blit(img2,(52,57))
    screen.blit(img3,(50,75))
    screen.blit(img4,(52,77))
    if(gameOver and self.game.score >= self.game.winScore):
      font2 = pg.font.SysFont(None,50)
      text1 = font2.render('Boo yah!',True, (0,0,0))
      text2 = font2.render('Boo yah!',True, (255,255,255))
      text11 = font.render('What are creatures of the night afraid of? YOU!!!',True, (0,0,0))
      text22 = font.render('What are creatures of the night afraid of? YOU!!!',True, (255,255,255))
      text3 = font.render('Press Enter to restart or BACKSPACE to End the game',True, (0,0,0))
      text4 = font.render('Press Enter to restart or BACKSPACE to End the game',True, (255, 255, 255))
      text_rect1 = text1.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5 - 27))
      text_rect2 = text2.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 - 25))
      text_rect11 = text11.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5 + 0))
      text_rect22 = text22.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 + 2))
      text_rect3 = text3.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5 + 20))
      text_rect4 = text4.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 + 22))
      screen.blit(text1,text_rect1)
      screen.blit(text2,text_rect2)
      screen.blit(text11,text_rect11)
      screen.blit(text22,text_rect22)
      screen.blit(text3,text_rect3)
      screen.blit(text4,text_rect4)
    elif(gameOver and self.game.score < self.game.winScore):
      font2 = pg.font.SysFont(None,50)
      text1 = font2.render('Love at first bite?',True, (0,0,0))
      text2 = font2.render('Love at first bite?',True, (255,255,255))
      text11 = font.render('Nope. Better luck next time!',True, (0,0,0))
      text22 = font.render('Nope. Better luck next time!',True, (255,255,255))
      text3 = font.render('Press Enter to restart or BACKSPACE to End the game',True, (0,0,0))
      text4 = font.render('Press Enter to restart or BACKSPACE to End the game',True, (255, 255, 255))
      text_rect1 = text1.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5 -22))
      text_rect2 = text2.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 - 20))
      text_rect11 = text11.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5))
      text_rect22 = text22.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 + 2))
      text_rect3 = text3.get_rect(center=(self.windowWidth*0.5, self.windowHeight*0.5 + 20))
      text_rect4 = text4.get_rect(center=(self.windowWidth*0.5 + 2, self.windowHeight*0.5 + 22))
      screen.blit(text1,text_rect1)
      screen.blit(text2,text_rect2)
      screen.blit(text11,text_rect11)
      screen.blit(text22,text_rect22)
      screen.blit(text3,text_rect3)
      screen.blit(text4,text_rect4)
