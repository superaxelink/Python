import pygame as py
import numpy as np
import time as tm
from pygame.locals import*

py.mixer.pre_init(44100, -16, 2, 512)
py.init()
py.mixer.init()
py.mixer.music.set_volume(0.2)
black = (0,0,0)
white = (255,255,255)
windowWidth = 1360
windowHeight	= 640
screen = py.display.set_mode((windowWidth,windowHeight))
py.display.set_caption('Side scroller')

class InputHandler():
  def __init__(self):
    self.keys = []
    self.touchY = ''
    self.touchThreshold = 30

  def checkEvent(self, player, enemies, gameOver):
    for event in py.event.get():
      if event.type == KEYDOWN:
        if(event.key == K_BACKSPACE):
          return False, not gameOver, []#return for gameOn, gameOver. Both are boolean and empty the list
        if(event.key == K_RETURN and gameOver): #to reset game
          player.restart()
          return True, not gameOver, [] #return for gameOn, gameOver. Both are boolean and restart enemy list
        if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT and self.keys.count(event.key) == 0):
          self.keys.append(event.key)
      elif event.type == KEYUP:
        if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT):
          self.keys.remove(event.key)
      elif event.type == QUIT:
        return False, not gameOver, [] #return for gameOn, gameOver. Both are boolean and empty the list
    return True, gameOver, enemies #return for gameOn, gameOver. Both are boolean and enemies.

class Player():
  def __init__(self,windowWidth,windowHeight):
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.width = 200
    self.height = 200
    self.x = 100 #starting point of player
    self.y = self.windowHeight - self.height
    self.image = py.image.load('player.png')
    self.frameX = 0
    self.maxFrame = 8
    self.frameY = 0
    self.fps = 20 #frames per second of player(how fast we swap between animation frames)
    self.frameTimer = 0#counter from 0 to frame interval over and over
    self.frameInterval = 1/self.fps #how many miliseconds each frame lasts
    self.speed = 0
    self.vy = 0
    self.weight = 1#how fast it will fall
  
  def restart(self):
    self.x = 100
    self.y = self.windowHeight - self.height 
    self.maxFrame = 8
    self.frameY = 0

  def draw(self,screen):
    crop = self.image.subsurface(self.width * self.frameX,self.height * self.frameY, self.width, self.height)
    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x, self.y))

  def update(self,input,deltaTime,enemies):
    #collision detection between squares
    for enemy in enemies:
      dx = (enemy.x + enemy.width * 0.5 - 20) - (self.x + self.width*0.5) #position of each enemy minus position of the player
      dy = (enemy.y + enemy.height * 0.5) - (self.y + self.height*0.5 + 20)
      distance = np.sqrt(dx*dx + dy*dy)
      if(distance < enemy.width/3 + self.width/3):
        return True #if there's a collision return true to the gameOver variable
    #sprite animation
    if(self.frameTimer > self.frameInterval):
      if(self.frameX >= self.maxFrame): self.frameX = 0
      else: self.frameX += 1
      self.frameTimer = 0 
    else:
      self.frameTimer += deltaTime
    #controls
    if(input.keys.count(K_RIGHT)>0):
      self.speed = 5
    elif(input.keys.count(K_LEFT)>0):
      self.speed = -5
    elif(input.keys.count(K_UP)>0 and self.onGround()):
      self.vy -= 29 #vertical jump
    else:
      self.speed = 0 
    #horizontal movement
    self.x += self.speed
    if(self.x < 0 ): self.speed = 0
    elif(self.x > self.windowWidth - self.width): self.x = self.windowWidth - self.width
    #vertical movement
    self.y += self.vy
    if(not self.onGround()):
      self.vy += self.weight #falling speed
      self.maxFrame = 5 #swap to jumping animaiton
      self.frameY = 1 #frame of animation on air
    else:
      self.vy = 0; #if it's on ground set vertical speed back to zero
      self.maxFrame = 8; #swap to running animation
      self.frameY = 0; #frame of animation on ground
    if(self.y > self.windowHeight - self.height): self.y = self.windowHeight - self.height
    return False #Return to keep the gameOver = False
  
  def onGround(self):
    return self.y >= self.windowHeight - self.height #condition to check if player is on ground or not 


class Background():
  def __init__(self,windowWidth,windowHeight):
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.x = 0
    self.y = 0
    self.width = 2400
    self.height = 720 #number of pixels of width and height of the image
    self.speed = 7 #horizontal coordinate of the background
    self.image = py.transform.scale(py.image.load('background_single.png'),(self.width,self.height)) #second scrooling background to fill the gap as the first image reset
			#accounting for horizontal speed in the second image help us to avoid little gaps between images
  def draw(self,screen):
    screen.blit(self.image,(self.x,self.y))
    screen.blit(self.image,(self.x + self.width,self.y))
  
  def update(self):
    self.x -= self.speed
    if(self.x < 0 - self.width): self.x = 0 #condition to reestart image

  def restart(self): #to restart background (and posssibly the game)
    self.x = 0

class Enemy():
  def __init__(self,windowWidth,windowHeight):
    self.windowWidth = windowWidth 
    self.windowHeight = windowHeight #width and height of canvas context 
    self.width = 160 
    self.height = 119 #width and height of enemy
    self.image = py.image.load('enemy_1.png') #enemy source
    self.x = self.windowWidth 
    self.y = self.windowHeight - self.height #horizontal and vertical coordinates of enemy
    self.frameX = 0 #to account which frame are we animating
    self.maxFrame = 5
    self.frameY = 0
    self.fps = 20 #frames per second of each individual enemy(how fast we swap between animation frames)
    self.frameTimer = 0#counter from 0 to frame interval over and over
    self.frameInterval = 1/self.fps #how many miliseconds each frame lasts
    self.speed = 8
    self.markedForDeletion = False

  def draw(self,screen):
    crop = self.image.subsurface(self.width * self.frameX,self.height * self.frameY, self.width, self.height)
    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x, self.y))

  def update(self,deltaTime,score):
    if(self.frameTimer > self.frameInterval):
      if(self.frameX >= self.maxFrame): self.frameX = 0
      else: self.frameX += 1
      self.frameTimer = 0 
    else:
      self.frameTimer += deltaTime
    self.x -= self.speed
    if(self.x < 0 - self.width):
      self.markedForDeletion = True
      score +=1
    return score

def handleEnemies(deltaTime,enemyTimer,score,enemies,gameOver):
  enemyInterval = 1 #threshold to be reached before adding a new enemy(in miliseconds)
  randomEnemyInterval = np.random.random() * 1 + 0.5 #to randomize interval in which add a new enemy
  if(enemyTimer > enemyInterval + randomEnemyInterval):
    enemies.append(Enemy(windowWidth, windowHeight))
    enemyTimer = 0
  else:
    enemyTimer += deltaTime
  for enemy in enemies:
    enemy.draw(screen)
    if(not gameOver):
      score = enemy.update(deltaTime,score)
  enemies = list(filter(lambda a : not a.markedForDeletion,enemies) )
  return enemyTimer, score, enemies

def drawStatus(screen,score,gameOver):# to draw status of the game
  font = py.font.SysFont(None,30)
  img1 = font.render('Score: ' + str(score),True, black)
  img2 = font.render('Score: ' + str(score),True, white)
  screen.blit(img1,(50,75))
  screen.blit(img2,(52,77))
  if(gameOver):
    font2 = py.font.SysFont(None,60)
    text1 = font2.render('GAME OVER, press Enter to restart or BACKSPACE to End the game',True, black)
    text2 = font2.render('GAME OVER, press Enter to restart or BACKSPACE to End the game',True, white)
    text_rect1 = text1.get_rect(center=(windowWidth*0.5, windowHeight*0.5))
    text_rect2 = text2.get_rect(center=(windowWidth*0.5 + 5, windowHeight*0.5 + 5))
    screen.blit(text1,text_rect1)
    screen.blit(text2,text_rect2)

input = InputHandler()
player = Player(windowWidth,windowHeight)
background = Background(windowWidth,windowHeight)

def animate(t0):
  gameOn = True
  gameOver = False
  enemyTimer = 0 #counter to add a new enemy
  score = 0
  enemies = []
  while gameOn:
    t1 = tm.perf_counter()
    deltaTime = t1 - t0
    t0 = t1
    screen.fill(white)
    gameOn, gameOver, enemies = input.checkEvent(player, enemies, gameOver)
    if(not gameOver):
      background.update()
      gameOver = player.update(input,deltaTime,enemies)
    background.draw(screen)
    player.draw(screen)
    enemyTimer, score, enemies = handleEnemies(deltaTime,enemyTimer,score,enemies,gameOver)
    #print(enemyTimer)
    drawStatus(screen,score,gameOver)
    py.display.flip()


animate(0)
