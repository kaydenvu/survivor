import pygame
import math
from random import randint as r

pygame.init()
C = pygame.time.Clock()

knight = pygame.image.load("player.png")
box = pygame.image.load("box.png")

GREEN = (35, 195, 40)
BLACK = (0, 0, 0)
SIZE = [500,500]
Screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Knight Survivor")
ITEMFONT = pygame.font.Font("pixel.ttf", 15)

V = pygame.math.Vector2
L = pygame.K_a
R = pygame.K_d
U = pygame.K_w
D = pygame.K_s

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__(ALL)
    self.pos = V(SIZE[0]/2, SIZE[1]/2)
    self.img = knight
    self.rect = self.img.get_rect(midbottom = self.pos)
    self.hitbox = self.rect.inflate(-82, -68)
    self.collectRadius = 75.0
  def draw(self):
    self.rect = self.img.get_rect(midbottom = self.pos)
    self.hitbox = self.rect.inflate(-82, -68)
    self.hitbox.right += 7
    Screen.blit(self.img, self.rect)
  def move(self):
    if K[R]:
      for entity in NOT_PLAYER:
        entity.pos.x -= 5
    if K[L]:
      for entity in NOT_PLAYER:
        entity.pos.x += 5
    if K[U]:
      for entity in NOT_PLAYER:
        entity.pos.y += 5
    if K[D]:
      for entity in NOT_PLAYER:
        entity.pos.y -= 5
  def collect(self):
    for item in ITEMS:
      dist = math.sqrt((item.pos.x-self.pos.x)**2 + (item.pos.y-self.pos.y)**2)
      if dist < self.collectRadius and not item.collected:
        item.pos -= (self.pos - item.pos) * .25
        item.collected = True
        item.timeSinceCollected = pygame.time.get_ticks()
  def update(self):
    self.draw()
    self.move()
    self.collect()

class PointDisplay(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__(ALL)
    self.pos = V(player.pos.x, player.pos.y-50)
    self.text = ITEMFONT.render("+1", True, BLACK)
    self.text.set_alpha(255)
  def draw(self):
    self.pos.y -= 3
    self.text.set_alpha(self.text.get_alpha()-10)
    Screen.blit(self.text, self.pos)
  def update(self):
    if self.text.get_alpha() <= 0:
      self.kill()
    else:
      self.draw()

class Item(pygame.sprite.Sprite):
  def __init__(self, type):
    super().__init__(ALL)
    super().__init__(NOT_PLAYER)
    super().__init__(ITEMS)
    self.alive = True
    self.collected = False
    self.pos = V(r(-1000, 1000), r(-500, 500))
    self.img = type
    self.rect = self.img.get_rect(center = self.pos)
    self.timeSinceCollected = 0.0
    if self.img == box:
      self.hitbox = self.rect.inflate(-85,-85)
      
  def goTowards(self):
    if not self.hitbox.colliderect(player.hitbox):
      self.pos += (player.pos - self.pos) * (.05 + (pygame.time.get_ticks() - self.timeSinceCollected)/1000)
    else:
      self.alive = False
      self.kill()
      PointDisplay()
      #print("collected")
  def draw(self):
    self.rect = self.img.get_rect(midbottom = self.pos)
    if self.img == box:
      #print("hi")
      self.hitbox = self.rect.inflate(-85,-85)
    #pygame.draw.rect(Screen, (0,0,0), self.hitbox)
    if self.alive:
      Screen.blit(self.img, self.rect)
  def update(self):
    self.draw()
    if self.collected and self.alive:
      self.goTowards()

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__(ALL)

ALL = pygame.sprite.Group()
NOT_PLAYER = pygame.sprite.Group()
ITEMS = pygame.sprite.Group()
player = Player()
for i in range(100):
  Item(box)

while True:
  C.tick(60)
  K = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      break
  Screen.fill(GREEN)
  ALL.update()
  print(player.pos)
  pygame.display.flip()