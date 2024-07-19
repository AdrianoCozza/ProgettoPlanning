from game.elevator_sprite import Elevator
import pygame

class InvisibleElevator(Elevator):
    def __init__(self):
        super().__init__(0, 0)
        self.image = pygame.image.load('imgs/empty.png')