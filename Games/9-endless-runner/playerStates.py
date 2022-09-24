from particles import Dust, Fire, Splash
states = {#stores possible states
  'SITTING': 0,
  'RUNNING': 1,
  'JUMPING': 2,
  'FALLING': 3,
  'ROLLING': 4,
  'DIVING': 5,
  'HIT': 6}

class State(): #base state class
  def __init__(self,state,game):
    self.state = state
    self.game = game

class Sitting(State):
  def __init__(self,game):
    super().__init__('SITTING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.game.player.frameX = 0
    self.game.player.maxFrame = 4
    self.game.player.frameY = 5

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input.count("ArrowLeft") != 0 or input.count("ArrowRight") !=0):
      self.game.player.setState(states['RUNNING'], 1)
    elif(input.count("Enter") != 0 or input.count(' ') != 0):
      self.game.player.setState(states['ROLLING'], 1.5)

class Running(State):
  def __init__(self,game):
    super().__init__('RUNNING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.game.player.frameX = 0
    self.game.player.maxFrame = 8
    self.game.player.frameY = 3

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    self.game.particles.append(Dust(self.game, self.game.player.x + self.game.player.width * 0.6, self.game.player.y + self.game.player.height))
    if(input.count("ArrowDown") != 0):
      self.game.player.setState(states['SITTING'], 0)
    elif(input.count("ArrowUp") != 0):
      self.game.player.setState(states['JUMPING'], 1)
    elif(input.count("Enter") != 0 or input.count(' ') != 0):
      self.game.player.setState(states['ROLLING'], 1.5)

class Jumping(State):
  def __init__(self,game):
    super().__init__('JUMPING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    if(self.game.player.onGround()): self.game.player.vy -= 8
    self.game.player.frameX = 0
    self.game.player.maxFrame = 6
    self.game.player.frameY = 1

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(self.game.player.vy > self.game.player.weight):
      self.game.player.setState(states['FALLING'], 1)
    elif(input.count("Enter") != 0 or input.count(' ') != 0):
      self.game.player.setState(states['ROLLING'], 1.5)
    elif(input.count("ArrowDown") != 0):
      self.game.player.setState(states['DIVING'], 0)

class Falling(State):
  def __init__(self,game):
    super().__init__('FALLING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.game.player.frameX = 0
    self.game.player.maxFrame = 6
    self.game.player.frameY = 2

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(self.game.player.onGround()):
      self.game.player.setState(states['RUNNING'], 1)
    elif(input.count("Enter") != 0 or input.count(' ') != 0):
      self.game.player.setState(states['ROLLING'], 1.5)
    elif(input.count("ArrowDown") != 0):
      self.game.player.setState(states['DIVING'], 0)

class Rolling(State):
  def __init__(self,game):
    super().__init__('ROLLING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.game.player.frameX = 0
    self.game.player.maxFrame = 6
    self.game.player.frameY = 6

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    self.game.particles.insert(0,Fire(self.game, self.game.player.x + self.game.player.width * 0.5, self.game.player.y + self.game.player.height*0.5))#add element to the beggining of the list
    if( (input.count('Enter') == 0 and input.count(' ') == 0) and self.game.player.onGround()):
      self.game.player.setState(states['RUNNING'], 1)
    elif( (input.count('Enter') == 0 and input.count(' ') == 0) and not self.game.player.onGround()):
      self.game.player.setState(states['FALLING'], 1)
    elif( (input.count('Enter') != 0 or input.count(' ') != 0) and input.count("ArrowUp") != 0  and self.game.player.onGround()):
      self.game.player.vy -= 8
    elif(input.count('ArrowDown') and not self.game.player.onGround()):
      self.game.player.setState(states['DIVING'],0)

class Diving(State):
  def __init__(self,game):
    super().__init__('DIVING',game)

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.game.player.frameX = 0
    self.game.player.maxFrame = 6
    self.game.player.frameY = 6
    self.game.player.vy = 12

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    self.game.particles.insert(0,Fire(self.game, self.game.player.x + self.game.player.width * 0.5, self.game.player.y + self.game.player.height*0.5))#add element to the beggining of the list
    if( self.game.player.onGround()):
      self.game.player.setState(states['RUNNING'], 1)
      for i in range(30):
        self.game.particles.insert(0, Splash(self.game, self.game.player.x + self.game.player.width * 0.5, self.game.player.y + self.game.player.height))
    elif((input.count('Enter') != 0 or input.count(' ') != 0) and self.game.player.onGround()):
      self.game.player.setState(states['ROLLING'], 1.5)

class Hit(State):
  def __init__(self,game):
    super().__init__("HIT",game)

  def enter(self):
    self.game.player.frameX = 0
    self.game.player.maxFrame = 10
    self.game.player.frameY = 4

  def handleInput(self,input):
    if(self.game.player.frameX >= 10 and self.game.player.onGround()):
      self.game.player.setState(states['RUNNING'],1)
    elif((input.count('Enter') != 0 or input.count(' ') != 0) and not self.game.player.onGround()):
      self.game.player.setState(states['FALLING'],1)
