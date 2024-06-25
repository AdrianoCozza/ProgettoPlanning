import pygame
from game.const import *
from game.elevator_sprite import Elevator
from game.passenger_sprite import Passenger
from game.floor_sprite import Floor
from pddl import Parser
import time

class Game:
    def __init__(self):
        # Running solver
        start = time.perf_counter()
        print('Running Solver')
        self.parser = Parser()
        elapsed = time.perf_counter() - start
        print(f'Solver done in {(elapsed * 1000):.2f} ms')

        # Initializing pygame data
        self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.floors = [int(SCREEN_HEIGHT * 0.85), int(SCREEN_HEIGHT * 0.5), int(SCREEN_HEIGHT * 0.15)]
        raw_people, current_floor = self.parser.get_people()
        self.current_floor = current_floor
        self.target_floor = self.current_floor
        self.moving = False
        self.elevator = Elevator(self.floors[self.current_floor])
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.elevator)

        # Must set this dynamically
        self.people = []
        target_x = {}
        for person_label, current_floor, target_floor in raw_people:
            if target_x.get(current_floor) is None:
                target_x[current_floor] = 20
            else:
                target_x[current_floor] += 30
            print(person_label, current_floor, target_floor)
            self.people.append(Passenger(x=target_x[current_floor], y=self.floors[current_floor], target_floor=target_floor, label=person_label))

        for person in self.people:
            self.all_sprites.add(person)

        for f in self.floors:
            self.all_sprites.add(Floor(0, f + self.people[0].rect.height))
        
        self.running = False
        self.clock = pygame.time.Clock()
        self.busy = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                """
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
                """
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_c:
                    self.handle_next_move()
                """
                elif event.key == pygame.K_r:
                    for person in self.elevator.passengers:
                        if person.target_floor == self.current_floor:
                            self.elevator.passengers.remove(person)
                            person.exit_elevator(self.floors[self.current_floor])
                """

    def pickup_person(self, person_label):
        for p in self.people:
            if p.label == person_label:
                p.enter_elevator(self.elevator)
    
    def move_elevator(self, direction):
        if direction == 'up':
            self.target_floor += 1
        elif direction == 'down':
            self.target_floor -= 1
        else:
            raise ValueError(f"Unknown direction: {direction}")
        self.moving = True

    def drop_passengers(self):
        for p in self.elevator.passengers:
            if p.target_floor == self.current_floor:
                self.elevator.passengers.remove(p)
                p.exit_elevator(self.floors[self.current_floor])

    def handle_next_move(self):
        if not self.parser.done():
            move, args = self.parser.next_move()
            print(move, args)
            if move == 'move-down':
                self.move_elevator('down')
            elif move == 'move-up':
                self.move_elevator('up')
            elif move == 'load':
                person_label, elevator_id = args
                self.pickup_person(person_label)
            elif move == 'unload':
                self.drop_passengers()
            

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

            if self.parser.done():
                break

        pygame.quit()