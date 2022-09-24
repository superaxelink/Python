import pygame as pg

class Layer():
  def __init__(self,game, width, height, speedModifier, image):
    self.game = game
    self.width = width
    self.height = height
    self.speedModifier = speedModifier
    self.image = image
    self.x = 0
    self.y = 0

  def update(self):
    if(self.x < -self.width): self.x = 0
    else: self.x -= self.game.speed * self.speedModifier

  def draw(self,screen):
    screen.blit(self.image,(self.x,self.y))
    screen.blit(self.image,(self.x + self.width,self.y))

class Background():
  def __init__(self, game):
    self.game = game
    self.width = 1667
    self.height = 500
    self.layer1image = pg.image.load('assets/layer-city-1.png').convert_alpha() 
    self.layer2image = pg.image.load('assets/layer-city-2.png').convert_alpha()
    self.layer3image = pg.image.load('assets/layer-city-3.png').convert_alpha()
    self.layer4image = pg.image.load('assets/layer-city-4.png').convert_alpha()
    self.layer5image = pg.image.load('assets/layer-city-5.png').convert_alpha()
    self.layer1 = Layer(self.game, self.width, self.height, 0, self.layer1image)
    self.layer2 = Layer(self.game, self.width, self.height, 0.2, self.layer2image)
    self.layer3 = Layer(self.game, self.width, self.height, 0.4, self.layer3image)
    self.layer4 = Layer(self.game, self.width, self.height, 0.8, self.layer4image)
    self.layer5 = Layer(self.game, self.width, self.height, 1, self.layer5image)
    self.backgroundLayers = [self.layer1, self.layer2, self.layer3, self.layer4, self.layer5]

  def update(self):
    for layer in self.backgroundLayers:
      layer.update()

  def draw(self,screen):
    for layer in self.backgroundLayers:
      layer.draw(screen)