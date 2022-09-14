states = {#stores possible states
  'STANDING_LEFT': 0,
  'STANDING_RIGHT': 1,
  'SITTING_LEFT': 2,
  'SITTING_RIGHT': 3,
  'RUNNING_LEFT': 4,
  'RUNNING_RIGHT': 5,
  'JUMPING_LEFT': 6,
  'JUMPING_RIGHT': 7,
  'FALLING_LEFT': 8,
  'FALLING_RIGHT': 9}

class State(): #base state class
  def __init__(self,state):
    self.state = state

class StandingLeft(State):
  def __init__(self,player):
    super().__init__('STANDING LEFT')
    self.player = player

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.player.frameY = 1
    self.player.speed = 0
    self.player.maxFrame = 6

  def handleInput(self,input):#to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS right'): self.player.setState(states['RUNNING_RIGHT'])
    #go to STANDING_RIGHT state if we press right
    elif(input == 'PRESS left'): self.player.setState(states['RUNNING_LEFT'])
    elif(input == 'PRESS down'): self.player.setState(states['SITTING_LEFT'])
    elif(input == 'PRESS up'): self.player.setState(states['JUMPING_LEFT'])

class StandingRight(State):
  def __init__(self,player):
    super().__init__('STANDING RIGHT')
    self.player = player
  
  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.player.frameY = 0
    self.player.speed = 0
    self.player.maxFrame = 6

  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS left'): self.player.setState(states['RUNNING_LEFT'])
    #go to STANDING_LEFT state if we press left
    elif(input == 'PRESS right'): self.player.setState(states['RUNNING_RIGHT'])
    elif(input == 'PRESS down'): self.player.setState(states['SITTING_RIGHT'])
    elif(input == 'PRESS up'): self.player.setState(states['JUMPING_RIGHT'])

class SittingLeft(State):
  def __init__(self, player):
    super().__init__('SITTING LEFT')
    self.player = player

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.player.frameY = 9
    self.player.speed = 0
    self.player.maxFrame = 4

  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS right'): self.player.setState(states['SITTING_RIGHT'])
    #go to STANDING_RIGHT state if we press right
    elif(input == 'PRESS up'): self.player.setState(states['STANDING_LEFT'])
    elif(input == 'RELEASE down'): self.player.setState(states['STANDING_LEFT'])

class SittingRight(State):
  def __init__(self,player):
    super().__init__('SITTING RIGHT')
    self.player = player

  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.player.frameY = 8
    self.player.speed = 0
    self.player.maxFrame = 4
  
  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS left'): self.player.setState(states['SITTING_LEFT'])
    #go to STANDING_RIGHT state if we press right
    elif(input == 'PRESS up'): self.player.setState(states['STANDING_RIGHT'])
    elif(input == 'RELEASE down'): self.player.setState(states['STANDING_RIGHT'])

class RunningLeft(State):
  def __init__(self,player):
    super().__init__('RUNNING LEFT')
    self.player = player
  
  def enter(self): #this will do everything that needs to be done when player
#enters this particular state
    self.player.frameY = 7
    self.player.speed = -self.player.maxSpeed
    self.player.maxFrame = 8

  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS right'): self.player.setState(states['RUNNING_RIGHT'])
    #go to STANDING_RIGHT state if we press right
    elif(input == 'PRESS up'): self.player.setState(states['JUMPING_LEFT'])
    elif(input == 'RELEASE left'): self.player.setState(states['STANDING_LEFT'])
    elif(input == 'PRESS down'): self.player.setState(states['SITTING_LEFT'])

class RunningRight(State):
  def __init__(self,player):
    super().__init__('RUNNING RIGHT')
    self.player = player
  
  def enter(self): #this sets 
    self.player.frameY = 6
    self.player.speed = self.player.maxSpeed
    self.player.maxFrame = 8

  def handleInput(self,input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS left'): self.player.setState(states['RUNNING_LEFT'])
    #go to STANDING_RIGHT state if we press right
    elif(input == 'PRESS up'): self.player.setState(states['JUMPING_RIGHT'])
    elif(input == 'RELEASE right'): self.player.setState(states['STANDING_RIGHT'])
    elif(input == 'PRESS down'): self.player.setState(states['SITTING_RIGHT'])

class JumpingLeft(State):
  def __init__(self,player):
    super().__init__('JUMPING LEFT')
    self.player = player

  def enter(self): #this sets 
    self.player.frameY = 3
    if(self.player.onGround()): self.player.vy -= 5 
    self.player.speed = -self.player.maxSpeed * 0.5
    self.player.maxFrame = 6
  
  def handleInput(self,input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS right'): self.player.setState(states['JUMPING_RIGHT'])
    elif(self.player.onGround()): self.player.setState(states['STANDING_LEFT'])
    elif(self.player.vy > 0): self.player.setState(states['FALLING_LEFT'])

class JumpingRight(State):
  def __init__(self,player):
    super().__init__('JUMPING RIGHT')
    self.player = player

  def enter(self): #this sets 
    self.player.frameY = 2
    if(self.player.onGround()): self.player.vy -= 5
    self.player.speed = self.player.maxSpeed * 0.5
    self.player.maxFrame = 6

  def handleInput(self,input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS left'): self.player.setState(states['JUMPING_LEFT'])
    elif(self.player.onGround()): self.player.setState(states['STANDING_RIGHT'])
    elif(self.player.vy > 0): self.player.setState(states['FALLING_RIGHT'])

class FallingLeft(State):
  def __init__(self,player):
    super().__init__('FALLING LEFT')
    self.player = player

  def enter(self): #this sets 
    self.player.frameY = 5
    self.player.maxFrame = 6

  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS right'): self.player.setState(states['FALLING_RIGHT'])
    elif(self.player.onGround()): self.player.setState(states['STANDING_LEFT'])

class FallingRight(State):
  def __init__(self,player):
    super().__init__('FALLING RIGHT')
    self.player = player

  def enter(self): #this sets 
    self.player.frameY = 4
    self.player.maxFrame = 6

  def handleInput(self, input): #to listen to a predefined set of inputs and swap
#to different state when the correct key is pressed
    if(input == 'PRESS left'): self.player.setState(states['FALLING_LEFT'])
    elif(self.player.onGround()): self.player.setState(states['STANDING_RIGHT'])