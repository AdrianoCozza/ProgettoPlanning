import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ELEVATOR_COLOR = (150, 150, 150)
PERSON_COLOR = (100, 100, 250)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elevator Simulation")

# Elevator dimensions and positions
ELEVATOR_WIDTH = 50
ELEVATOR_HEIGHT = 100
elevator_x = (SCREEN_WIDTH - ELEVATOR_WIDTH) // 2
elevator_y = SCREEN_HEIGHT - ELEVATOR_HEIGHT

# Person dimensions
PERSON_WIDTH = 20
PERSON_HEIGHT = 20

# Floors
floors = [100, 300, 500]
current_floor = 2
target_floor = None
moving = False

# People
people = [
    {"x": 20, "y": floors[0], 'color': (255, 0, 0)},
    {"x": 20, "y": floors[1], 'color': (0, 255, 0)},
    {"x": 20, "y": floors[2], 'color': (255, 0, 250)}
]

# Helper function to draw the elevator
def draw_elevator(x, y):
    pygame.draw.rect(screen, ELEVATOR_COLOR, (x, y, ELEVATOR_WIDTH, ELEVATOR_HEIGHT))

# Helper function to draw people
def draw_people(people):
    for person in people:
        pygame.draw.rect(screen, person['color'], (person["x"], person["y"], PERSON_WIDTH, PERSON_HEIGHT))

people_in_elevator = []

# Function to move elevator
def move_elevator():
    global elevator_y, moving, current_floor
    if target_floor is not None:
        target_y = floors[target_floor]
        if elevator_y < target_y:
            elevator_y += 5
            if elevator_y >= target_y:
                elevator_y = target_y
                moving = False
                current_floor = target_floor
        elif elevator_y > target_y:
            elevator_y -= 5
            if elevator_y <= target_y:
                elevator_y = target_y
                moving = False
                current_floor = target_floor
    for p in people_in_elevator:
        p['y'] = elevator_y

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                target_floor = 0
                moving = True
            elif event.key == pygame.K_2:
                target_floor = 1
                moving = True
            elif event.key == pygame.K_3:
                target_floor = 2
                moving = True
            elif event.key == pygame.K_SPACE:
                if current_floor is not None:
                    for person in people:
                        if person["y"] == floors[current_floor]:
                            person["x"] = elevator_x + ELEVATOR_WIDTH / 2
                            if person not in people_in_elevator:
                                people_in_elevator.append(person)
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                p = people_in_elevator.pop()
                p['x'] = 20

    # Move the elevator
    if moving:
        move_elevator()

    # Clear screen
    screen.fill(WHITE)

    # Draw elevator and people
    draw_elevator(elevator_x, elevator_y)
    draw_people(people)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()