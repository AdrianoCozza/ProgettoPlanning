import pygame
import random

# Initialize Pygame
pygame.init()

# load sound 
elevator_ding = pygame.mixer.Sound('sounds/elevator_ding.wav')


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
elevator_image = pygame.image.load('imgs/elevator.png')
elevator_image = pygame.transform.scale(elevator_image, (int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.2)))

background_image = pygame.image.load('imgs/hotel.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Elevator sprite
class Elevator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = elevator_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = floors[current_floor] - self.rect.height / 2
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

# Person sprite
class Person(pygame.sprite.Sprite):

    def __init__(self, x, y, weight, priority, target_floor):
        super().__init__()
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
        self.weight = weight
        self.priority = priority
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

# Initialize elevator
elevator = Elevator()  # Adjust max weight as needed
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
                        person.exit_elevator(floors[current_floor])
                        #person.rect.y = floors[current_floor]  # Set the person to the current floor

    # Move the elevator
    if moving and target_floor is not None:
        moving = elevator.move(floors[target_floor])
        if not moving:
            current_floor = target_floor
            elevator_ding.play()

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    for p in people:
        p.step_all_animations()
    
pygame.quit()
