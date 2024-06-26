import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ELEVATOR_CLOSED_IMAGE = pygame.image.load('imgs/elevator.png')
ELEVATOR_CLOSED_IMAGE = pygame.transform.scale(ELEVATOR_CLOSED_IMAGE, (70, 80))
ELEVATOR_OPEN_IMAGE = pygame.image.load('imgs/elevator_open.png')
ELEVATOR_OPEN_IMAGE = pygame.transform.scale(ELEVATOR_OPEN_IMAGE, (70, 80))
ELEVATOR_SOUND = pygame.mixer.Sound('sounds/elevator_ding.wav')

BACKGROUND_IMAGE = pygame.image.load('imgs/background_w_text.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

MIN_DELAY_BETWEEN_MOVES = 1 # Expressed in seconds