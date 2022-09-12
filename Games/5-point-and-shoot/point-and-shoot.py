from pickle import TRUE
import pygame as py
import numpy as np
import time as tm
from pygame.locals import*

py.mixer.pre_init(44100, -16, 2, 512)
py.init()
py.mixer.init()
py.mixer.music.set_volume(0.2)
score = 0
gameOver = False
gameOn = True
squares = False
deltaTime = 0
timeToNextRaven = 0
ravenInterval = 2
lastTime = 0
ravens = []
explosions = []
particles = []
general = []
windowWidth = 800
windowHeight = 500
black = (0,0,0)
white = (255,255,255)
sound = py.mixer.Sound("f-i.wav") 
screen = py.display.set_mode((windowWidth,windowHeight))
py.display.set_caption('Collision Animations')

class Raven():
  def __init__(self):
    self.spriteWidth = 271
    self.spriteHeight = 194 
    self.sizeModifier = np.random.random() * 0.6 + 0.4
    self.width = self.spriteWidth * self.sizeModifier
    self.height = self.spriteHeight * self.sizeModifier
    self.x = windowWidth + self.width
    self.y = (windowHeight - self.height)*np.random.random() 
    self.directionX = np.random.random()*2 +0.5
    self.directionY = np.random.random()*3 - 1.5
    self.markedForDeletion = False
    self.image =py.image.load("raven.png")
    self.frame = 0
    self.maxFrame = 4
    self.timeSinceFlap = 0
    self.timer = 0
    self.fps = 20
    self.falpInterval = (3 + 0.5*np.random.random())/self.fps
    self.color = (np.floor(np.random.random()*255),np.floor(np.random.random()*255),np.floor(np.random.random()*255))
    self.rect = py.Surface((self.width,self.height))
    self.hasTrail = np.random.random() > 0.5
  def update(self,deltaTime):
    global gameOver
    #To control what to do on the edges of the screen
    if(self.y < 0 or self.y + self.height > windowHeight):
      self.directionY = self.directionY*(-1)
    self.x -= self.directionX
    self.y += self.directionY
    if(self.x <0 - self.width):  
      self.markedForDeletion = True
      gameOver = True
    #To control how to procceed to next animation
    self.timeSinceFlap += deltaTime
    if(self.timeSinceFlap > self.falpInterval):
      if(self.frame>self.maxFrame): self.frame = 0
      else: self.frame += 1
      self.timeSinceFlap = 0
      #To add particles
      i=0
      if(self.hasTrail):
        while i<5:
          particles.append(Particle(self.x, self.y, self.width, self.color))
          i += 1 
    if(self.x<0 - self.width): gameOver = True
  def draw(self,screen):
    if(squares): #activate and deactive square visualization
      self.rect.set_alpha(100)
      self.rect.fill(self.color)
      screen.blit(self.rect,(self.x - self.width*0.5,self.y))
    crop = self.image.subsurface(self.spriteWidth * self.frame,0,self.spriteWidth,self.spriteHeight)

    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x - self.width*0.5,self.y))
    

class Explosion():
  def __init__(self,x,y,size):
    self.image = py.image.load("boom.png")
    self.spriteWidth = 200
    self.spriteHeight = 175
    self.size = size
    self.width = self.size
    self.height = self.size
    self.x = x
    self.y = y
    self.maxFrame = 4
    self.frame = 0
    self.timeSinceLastFrame = 0
    self.frameInterval = 0.1
    self.markedForDeletion = False
  def update(self,deltaTime):
    if(self.frame == 0):
      py.mixer.Sound.stop(sound)
      py.mixer.Sound.play(sound)
    self.timeSinceLastFrame += deltaTime
    if(self.timeSinceLastFrame > self.frameInterval):
      self.frame += 1
      self.timeSinceLastFrame = 0
      if(self.frame == self.maxFrame):
        self.markedForDeletion = True
  def draw(self,screen):
    crop = self.image.subsurface(self.spriteWidth * self.frame,0,self.spriteWidth,self.spriteHeight)
    screen.blit(py.transform.scale(crop,(self.width,self.height)),(self.x - self.width*0.5,self.y - self.width*0.5))

class Particle():
  def __init__(self,x,y,size,color):
    self.size = size
    self.x = x + self.size*0.5 + np.random.random()*50 - 25
    self.y = y + self.size*0.33333333333 + np.random.random()*50 - 25
    self.radius = np.random.random()*self.size*0.1
    self.maxRadius = np.random.random()*20 + 35
    self.markedForDeletion = False
    self.speedX =  np.random.random()*1 + 0.5
    self.color = color
    #width and height of the surface to create the circular particles
    self.circ = py.Surface((2*self.radius,2*self.radius), py.SRCALPHA) 
  def update(self,deltaTime):
    self.x += self.speedX
    self.radius += 0.2
    if(self.radius > self.maxRadius - 3):#condition to delete the particle
      self.markedForDeletion = True
  def draw(self,screen): #to update the circular particles with the parameter set to include a difumination alpha
    self.circ = py.Surface((2*self.radius,2*self.radius), py.SRCALPHA)
    alpha=(1-self.radius/self.maxRadius)*255 #difumination of the color color
    #this includes as parameters the surface, the color with the difumination alpha, position in where we want
    #to draw the circle IN THE  NEW AREA and the radius of the circle
    py.draw.circle(self.circ,(self.color + (alpha,)),(self.radius,self.radius),self.radius)
    #surface we are goint to blit into the main surface and position in which it will be drawn
    screen.blit(self.circ,(self.x-self.radius,self.y-self.radius))
     
#to draw gradient
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    #"""fill a surface with a gradient pattern
    #Parameters:
    #color -> starting color
    #gradient -> final color
    #rect -> area to fill; default is surface's rect
    #vertical -> True=vertical; False=horizontal
    #forward -> True=forward; False=reverse
    # 
    #Pygame recipe: http://www.pygame.org/wiki/GradientCode
    #"""
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = py.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

def drawScore(screen): #To draw the score
  font = py.font.SysFont(None,30)
  img1 = font.render('Score: ' + str(score),True, black)
  img2 = font.render('Score: ' + str(score),True, white)
  screen.blit(img1,(50,75))
  screen.blit(img2,(52,77))

def drawGameOver(screen):# to draw the game over message
  font = py.font.SysFont(None,60)
  font2 = py.font.SysFont(None,30)
  text1 = font.render('GAME OVER, your score is ' + str(score),True, black)
  text2 = font.render('GAME OVER, your score is ' + str(score),True, white)
  text3 = font2.render('Press R to restart or E to End the game',True, black)
  text4 = font2.render('Press R to restart or E to End the game',True, white)
  text_rect1 = text1.get_rect(center=(windowWidth*0.5, windowHeight*0.5))
  text_rect2 = text2.get_rect(center=(windowWidth*0.5 + 5, windowHeight*0.5 + 5))
  text_rect3 = text1.get_rect(center=(windowWidth*0.5 + 92, windowHeight*0.5 + 60))
  text_rect4 = text2.get_rect(center=(windowWidth*0.5 + 92, windowHeight*0.5 + 60 + 2))
  screen.blit(text1,text_rect1)
  screen.blit(text2,text_rect2)
  screen.blit(text3,text_rect3)
  screen.blit(text4,text_rect4)

def checkClick(mouse,ravens):#to detect when clicking on proper area
  global score
  positionX = mouse[0] 
  positionY = mouse[1] 
  for object in ravens:
    if (positionX > object.x - object.width*0.5 and positionX < object.x + object.width*0.5 and positionY > object.y and positionY < object.y + object.height):
      object.markedForDeletion = True
      score += 1  
      explosions.append(Explosion(positionX,positionY,object.width))

def Restart():
  global score
  global timeToNextRaven
  global particles
  global ravens
  global general
  global explosions
  global gameOver
  score = 0
  timeToNextRaven = 0
  gameOver = False
  particles.clear()
  ravens.clear()
  explosions.clear()
  general.clear()

#Main animate function
def animate(deltaTime):
  global gameOn
  global timeToNextRaven
  global squares
  global particles
  global ravens
  global general
  global explosions
  while gameOn:
    general.clear()
    t0 = tm.perf_counter()
    for event in py.event.get():
      if (event.type == MOUSEBUTTONDOWN and not gameOver):
        checkClick(py.mouse.get_pos(),ravens)
      if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
          gameOn = False
        elif event.key == K_d and squares == False:
          squares = True
        elif event.key == K_d and squares == True:
          squares = False
        elif (event.key == K_r and gameOver):
          Restart()
        elif (event.key == K_e and gameOver):
          gameOn = False
      elif event.type == QUIT:
        gameOn = False
    screen.fill(white)
    fill_gradient(screen,(0,255,0),(0,0,255))
    if(not gameOver):
      timeToNextRaven += deltaTime

      #CLEAN THE LISTS
      particles = list(filter(lambda a : not a.markedForDeletion,particles) )
      ravens = list(filter(lambda a : not a.markedForDeletion,ravens) )
      explosions = list(filter(lambda a : not a.markedForDeletion, explosions) )
    
      #TIME TO CREATE NEXT RAVEN
      if(timeToNextRaven > ravenInterval):
        ravens.append(Raven())
        timeToNextRaven = 0
        ravens.sort(key= lambda a : a.width)
    
    #ADD RAVENS TO GENERAL LIST TO MANAGE UPDATES AND DRAWS
    general.append(particles)
    general.append(ravens)
    general.append(explosions)  
    general = sum(general,[]) #to flatten the list
    #print(len(general))
    drawScore(screen)
    #UPDATE AND DRAW ALL OBJECTS IN GENERAL LIST
    for object in general:
      if(not gameOver):
        object.update(deltaTime)
      object.draw(screen)

    if(gameOver):
      drawGameOver(screen)
    py.display.flip()
    deltaTime = tm.perf_counter() - t0
    #print("FINISHED")

animate(deltaTime)