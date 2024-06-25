import pygame
from game.const import *
from game.elevator_sprite import Elevator
from game.passenger_sprite import Passenger
from game.floor_sprite import Floor
from pddl import run_program_and_parse_output

class Game:
    def __init__(self):
        # Running solver
        print('Running Solver')
        self.moves = run_program_and_parse_output()
        print('Solver done')

        # Initializing pygame data
        self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.floors = [int(SCREEN_HEIGHT * 0.85), int(SCREEN_HEIGHT * 0.5), int(SCREEN_HEIGHT * 0.15)]
        self.current_floor = 2
        self.target_floor = None
        self.moving = False
        self.elevator = Elevator(self.floors[2])
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.elevator)

        # Must set this dynamically
        self.people = [
            Passenger(x=20, y=self.floors[0], target_floor=1, label='PersonA'),
            Passenger(x=50, y=self.floors[0], target_floor=2, label='PersonB'),
            Passenger(x=20, y=self.floors[1], target_floor=2, label='PersonC'),
            Passenger(x=80, y=self.floors[0], target_floor=1, label='PersonD'),
            Passenger(x=20, y=self.floors[2], target_floor=0, label='PersonE'),
        ]

        for person in self.people:
            self.all_sprites.add(person)

        for f in self.floors:
            self.all_sprites.add(Floor(0, f + self.people[0].rect.height))
        
        self.running = False
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.target_floor = 0
                    self.moving = True
                elif event.key == pygame.K_2:
                    self.target_floor = 1
                    self.moving = True
                elif event.key == pygame.K_3:
                    self.target_floor = 2
                    self.moving = True
                elif event.key == pygame.K_SPACE:
                    if self.current_floor is not None:
                        for person in self.people:
                            if person.rect.y == self.floors[self.current_floor] and not person.in_elevator and person.target_floor != self.current_floor:
                                person.enter_elevator(self.elevator)
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r:
                    for person in self.elevator.passengers:
                        if person.target_floor == self.current_floor:
                            self.elevator.passengers.remove(person)
                            person.exit_elevator(self.floors[self.current_floor])

    def update_frame(self):
        # Reset frame
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        self.clock.tick(FPS)
        
        for p in self.people:
            p.step_all_animations()

    def main_loop(self):
        pygame.display.set_caption("Elevator Simulation")
        self.running = True
        
        while self.running:
            self.handle_events()

            if self.moving and self.target_floor is not None:
                moving = self.elevator.move(self.floors[self.target_floor])
                if not moving:
                    self.current_floor = self.target_floor
                    ELEVATOR_SOUND.play()
            
            self.update_frame()
        
        self.running = False
        pygame.quit()