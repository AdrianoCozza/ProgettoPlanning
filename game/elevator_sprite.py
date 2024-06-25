import pygame
from game.const import *

class Elevator(pygame.sprite.Sprite):
    def __init__(self, current_floor_y):
        super().__init__()
        self.image = ELEVATOR_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = current_floor_y - self.rect.height / 2
        self.passengers = []

    def move(self, target_y):
        previous_rect_y = self.rect.y
        if self.rect.centery < target_y:
            self.rect.y += 5
            if self.rect.centery >= target_y:
                self.rect.y = target_y - self.rect.height / 2
                return False
        elif self.rect.centery > target_y:
            self.rect.y -= 5
            if self.rect.centery <= target_y:
                self.rect.y = target_y - self.rect.height / 2
                return False

        for p in self.passengers:
            p.rect.y += self.rect.y - previous_rect_y
        return True