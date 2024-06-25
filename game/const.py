import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ELEVATOR_IMAGE = pygame.image.load('imgs/elevator.png')
ELEVATOR_IMAGE = pygame.transform.scale(ELEVATOR_IMAGE, (int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.2)))
ELEVATOR_SOUND = pygame.mixer.Sound('sounds/elevator_ding.wav')

BACKGROUND_IMAGE = pygame.image.load('imgs/background_w_text.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))