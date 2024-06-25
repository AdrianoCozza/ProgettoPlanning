import pygame
import random
from game.const import *

class Passenger(pygame.sprite.Sprite):

    def __init__(self, x, y, target_floor, label):
        super().__init__()
        self.label = label

        all_colors = [ 'blue', 'yellow', 'red' ]
        random_chosen_color = all_colors[random.randint(0, len(all_colors)-1)]
        self.IMAGES = {
            'WALKING': [f'imgs/passengers/{random_chosen_color}_guy_walking_1.png', f'imgs/passengers/{random_chosen_color}_guy_walking_2.png'],
            'BASE': f'imgs/passengers/{random_chosen_color}_guy_walking_0.png'
        }
        img = pygame.image.load(self.IMAGES['BASE'])
        img = pygame.transform.scale(img, (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.05)))
        self.base_image = img
        self.image = img
        self.walking_animation_imgs = []
        for img_path in self.IMAGES['WALKING']:
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.05)))
            self.walking_animation_imgs.append(img)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_floor = target_floor
        self.in_elevator = False
        self.target_x = -1
        self.target_y = -1
        self.run_walking_animation = False
        self.steps = 50
        self.current_step = 0
        self.is_running_backwards = False

    def enter_elevator(self, elevator):
        if not self.in_elevator:
            elevator.passengers.append(self)
            self.in_elevator = True
            self.run_walking_animation = True
            self.target_x = elevator.rect.x + 10 + len(elevator.passengers) * 20
            self.current_step = 0
            self.step_size = abs(self.rect.x - self.target_x) / self.steps
            self.is_running_backwards = False
    
    def step_walking_animation(self):
        self.image = self.walking_animation_imgs[self.current_step % len(self.walking_animation_imgs)]
        if self.is_running_backwards:
            self.image = pygame.transform.flip(self.image, 1, 0)

        self.current_step += 1
        self.rect.x += self.step_size
        if self.current_step == self.steps and not self.is_running_backwards:
            self.run_walking_animation = False
            self.image = self.base_image
            self.current_step = 0
            self.image = pygame.transform.flip(self.image, 1, 0)

    def step_all_animations(self):
        if self.run_walking_animation:
            self.step_walking_animation()

    def exit_elevator(self, floor):
        if self.in_elevator:
            #self.rect.x = 20 + len([p for p in people if not p.in_elevator]) * 30
            self.rect.y = floor
            self.in_elevator = False
            self.target_x = -1
            self.run_walking_animation = True
            self.current_step = 0
            self.step_size = -10
            self.is_running_backwards = True

    def __str__(self):
        return f"Person(target_floor={self.target_floor}), in_elevator={self.in_elevator})"