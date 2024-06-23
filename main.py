import pygame
import random

# Initialize Pygame
pygame.init()

# Get screen information
info = pygame.display.Info()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define some constants
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elevator Simulation")

# Floors
floors = [int(SCREEN_HEIGHT * 0.85), int(SCREEN_HEIGHT * 0.5), int(SCREEN_HEIGHT * 0.15)]
current_floor = 2
target_floor = None
moving = False

# Load and scale images
elevator_image = pygame.image.load('elevator.png')
elevator_image = pygame.transform.scale(elevator_image, (int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.2)))

background_image = pygame.image.load('hotel.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Elevator sprite
class Elevator(pygame.sprite.Sprite):
    def __init__(self, max_weight):
        super().__init__()
        self.image = elevator_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = floors[current_floor]
        self.passengers = []
        self.max_weight = max_weight
        self.current_weight = 0

    def move(self, target_y):
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
        for i, passenger in enumerate(self.passengers):
            passenger.rect.y = self.rect.y + 10 + i * 20
        return True

# Person sprite
class Person(pygame.sprite.Sprite):
    IMAGES = {
        'WALKING': ['guy/guy_walking_1.png', 'guy/guy_walking_2.png'],
        'BASE': 'guy/guy_walking_0.png'
    }

    def __init__(self, x, y, weight, priority, target_floor):
        super().__init__()
        img = pygame.image.load(Person.IMAGES['BASE'])
        img = pygame.transform.scale(img, (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.05)))
        self.base_image = img
        self.image = img
        self.walking_animation_imgs = []
        for img_path in Person.IMAGES['WALKING']:
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.05)))
            self.walking_animation_imgs.append(img)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.weight = weight
        self.priority = priority
        self.target_floor = target_floor
        self.in_elevator = False
        self.target_x = -1
        self.target_y = -1
        self.run_walking_animation = False
        self.steps = 50
        self.current_step = 0

    def enter_elevator(self, elevator):
        if not self.in_elevator and (elevator.current_weight + self.weight <= elevator.max_weight):
            elevator.passengers.append(self)
            elevator.current_weight += self.weight
            self.in_elevator = True
            self.run_walking_animation = True
            self.target_x = elevator.rect.x + 10 + len(elevator.passengers) * 20
            self.current_step = 0
            self.step_size = abs(self.rect.x - self.target_x) / self.steps
    
    def step_animation(self):
        if not self.run_walking_animation:
            self.image = self.base_image
            return
        self.image = self.walking_animation_imgs[self.current_step % len(self.walking_animation_imgs)]
        self.current_step += 1
        self.rect.x += self.step_size
        if self.current_step == self.steps:
            self.run_walking_animation = False

    def exit_elevator(self, elevator):
        if self.in_elevator:
            self.rect.x = 20 + len([p for p in people if not p.in_elevator]) * 30
            elevator.current_weight -= self.weight
            self.in_elevator = False
    
    def __str__(self):
        return f"Person(target_floor={self.target_floor}), in_elevator={self.in_elevator})"

# Initialize elevator
elevator = Elevator(max_weight=300)  # Adjust max weight as needed
all_sprites = pygame.sprite.Group()
all_sprites.add(elevator)

# Initialize people
people = [
    Person(20, floors[0], weight=60, priority=1, target_floor=1),
    Person(20, floors[1], weight=70, priority=2, target_floor=2),
    Person(20, floors[2], weight=80, priority=1, target_floor=0)
]

for person in people:
    all_sprites.add(person)

# Function to determine the next target floor
def get_next_target_floor():
    if elevator.passengers:
        return min(elevator.passengers, key=lambda p: p.priority).target_floor
    return None

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
                        if person.rect.y == floors[current_floor] and not person.in_elevator and person.target_floor != current_floor:
                            person.enter_elevator(elevator)
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                for person in elevator.passengers:
                    if person.target_floor == current_floor:
                        elevator.passengers.remove(person)
                        person.exit_elevator(elevator)
                        person.rect.y = floors[current_floor]  # Set the person to the current floor



    # Move the elevator
    if moving and target_floor is not None:
        moving = elevator.move(floors[target_floor])
        if not moving:
            current_floor = target_floor

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    for p in people:
        p.step_animation()
    
pygame.quit()
