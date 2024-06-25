import pygame
from game.const import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imgs/floor.png')
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH / 2 - ELEVATOR_IMAGE.get_rect().width / 2, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y