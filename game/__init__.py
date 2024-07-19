import pygame
from game.const import *
from game.elevator_sprite import Elevator
from game.invisible_elevator_sprite import InvisibleElevator
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
        self.floors = []
        raw_people, current_floor_elevator_x, current_floor_elevator_y, num_floors = self.parser.get()

        if num_floors < 1 or num_floors > 4:
            print('Number of floors invalid: please specify a number of floors from 1-4')
            exit(1)
        
        floor_start_x = 10
        for i in range(num_floors):
            self.floors.append(int(SCREEN_HEIGHT * ( (num_floors - i) / 5) + floor_start_x))

        self.current_floor_elevator_x = current_floor_elevator_x
        self.target_floor_elevator_x = self.current_floor_elevator_x

        self.current_floor_elevator_y = current_floor_elevator_y
        self.target_floor_elevator_y = self.current_floor_elevator_y

        self.moving_elevator_x = False
        self.moving_elevator_y = False

        self.elevatorX = Elevator(self.floors[self.current_floor_elevator_x], (SCREEN_WIDTH - ELEVATOR_CLOSED_IMAGE.get_width()) // 1.675)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.elevatorX)

        if self.current_floor_elevator_y is not None:
            self.elevatorY = Elevator(self.floors[self.current_floor_elevator_y], 0)
        else:
            self.elevatorY = InvisibleElevator()

        self.all_sprites.add(self.elevatorY)
        
        self.people = []
        target_x = {}
        for person_label, current_floor_elevator_x, target_floor in raw_people:
            if target_x.get(current_floor_elevator_x) is None:
                target_x[current_floor_elevator_x] = 20
            else:
                target_x[current_floor_elevator_x] += 40
            self.people.append(Passenger(x=target_x[current_floor_elevator_x] + ELEVATOR_CLOSED_IMAGE.get_width(), y=self.floors[current_floor_elevator_x], target_floor=target_floor, label=person_label))

        for person in self.people:
            self.all_sprites.add(person)

        for f in self.floors:
            self.all_sprites.add(Floor(ELEVATOR_CLOSED_IMAGE.get_width(), f + self.people[0].rect.height))
        
        self.running = False
        self.clock = pygame.time.Clock()
        self.busy = False

        self.lines = []
        self.max_lines = 16

        self.visualization_paused = True
        self.last_move_update = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_c:
                    self.visualization_paused = not self.visualization_paused

    def pickup_person(self, person_label, elevator_id):
        for p in self.people:
            if p.label == person_label:
                if elevator_id == 'elevatorX':
                    p.enter_elevator(self.elevatorX)
                else:
                    p.enter_elevator(self.elevatorY)
    
    def move_elevator(self, direction, elevator_id):
        if elevator_id == 'elevatorX':
            if direction == 'up':
                self.target_floor_elevator_x += 1
            elif direction == 'down':
                self.target_floor_elevator_x -= 1
            else:
                raise ValueError(f"Unknown direction: {direction}")
            self.moving_elevator_x = True
        elif elevator_id == 'elevatorY':
            if direction == 'up':
                self.target_floor_elevator_y += 1
            elif direction == 'down':
                self.target_floor_elevator_y -= 1
            else:
                raise ValueError(f"Unknown direction: {direction}")
            self.moving_elevator_y = True
        else:
            raise ValueError(f"Unknown elevator: {elevator_id}")

    def passenger_leaves(self, person_label):
        to_remove = []
        for p in self.people:
            if p.label == person_label:
                p.reached()
                to_remove.append(p)
        
        for p in to_remove:
            self.people.remove(p)

    def unload_passenger(self, person_label, elevator_id):
        for p in self.elevatorX.passengers:
            if p.label == person_label:
                self.elevatorX.passengers.remove(p)
                p.unload_elevator(self.floors[self.current_floor_elevator_x], self.elevatorX.rect.centery)

        for p in self.elevatorY.passengers:
            if p.label == person_label:
                self.elevatorY.passengers.remove(p)
                p.unload_elevator(self.floors[self.current_floor_elevator_y], self.elevatorY.rect.centery)

    def handle_next_move(self):
        busy_flag = self.moving_elevator_x or self.moving_elevator_y
        for p in self.people:
            if p.run_walking_animation:
                busy_flag = True
                break

        # Give me a delay of at least 2 seconds between moves
        time_since_last_move = time.time() - self.last_move_update
        if time_since_last_move <= MIN_DELAY_BETWEEN_MOVES:
            busy_flag = True

        if not self.parser.done() and not busy_flag and not self.visualization_paused:
            idx, move, args = self.parser.next_move()
            txt = f'{idx} {move} {str(args)}'
            #print(txt)
            self.lines.append(txt)
            self.last_move_update = time.time()

            if len(self.lines) > self.max_lines:
                self.lines = self.lines[1:]

            if self.parser.done():
                self.lines.append('SOLVED')

            if len(self.lines) > self.max_lines:
                self.lines = self.lines[1:]

            if move == 'move-down':
                self.move_elevator('down', args[0])
            elif move == 'move-up':
                self.move_elevator('up', args[0])
            elif move == 'load':
                person_label, elevator_id = args
                self.pickup_person(person_label, elevator_id)
            elif move == 'unload':
                person_label, elevator_id = args
                self.unload_passenger(person_label, elevator_id)
            elif move == 'reached':
                self.passenger_leaves(*args)

    def update_frame(self):
        # Reset frame
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Render text
        font = pygame.font.Font(None, 20)
        for i, l in enumerate(self.lines):
            txt_surface = font.render(l, True, pygame.Color('white'))
            self.screen.blit(txt_surface, (SCREEN_WIDTH - txt_surface.get_width() / 2 - 160, i*20 + 140))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw passengers nametags
        spacing = 0
        for p in self.people:
            x = p.rect.x + p.rect.width / 2 - 10
            y = p.rect.centery - p.rect.height / 2 - 10
            if p in self.elevatorX.passengers and not p.run_walking_animation:
                x = self.elevatorX.rect.centerx + self.elevatorX.rect.width / 2
                y = self.elevatorX.rect.y + spacing
                spacing += 15
            
            if p in self.elevatorY.passengers and not p.run_walking_animation:
                x = self.elevatorY.rect.centerx + self.elevatorX.rect.width / 2
                y = self.elevatorY.rect.y + spacing
                spacing += 15

            self.screen.blit(p.nametag, (x, y))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        self.clock.tick(FPS)
        
        for p in self.people:
            p.step_all_animations()

    def draw_text(screen, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def main_loop(self):
        pygame.display.set_caption("Elevator Simulation")
        self.running = True
        
        while self.running:
            self.handle_events()

            if self.moving_elevator_x and self.target_floor_elevator_x is not None:
                self.elevatorX.image = ELEVATOR_CLOSED_IMAGE
                self.moving_elevator_x = self.elevatorX.move(self.floors[self.target_floor_elevator_x])
                if not self.moving_elevator_x:
                    self.elevatorX.image = ELEVATOR_OPEN_IMAGE
                    self.current_floor_elevator_x = self.target_floor_elevator_x
                    ELEVATOR_SOUND.play()
            
            if self.moving_elevator_y and self.target_floor_elevator_y is not None:
                self.elevatorY.image = ELEVATOR_CLOSED_IMAGE
                self.moving_elevator_y = self.elevatorY.move(self.floors[self.target_floor_elevator_y])
                if not self.moving_elevator_y:
                    self.elevatorY.image = ELEVATOR_OPEN_IMAGE
                    self.current_floor_elevator_y = self.target_floor_elevator_y
                    ELEVATOR_SOUND.play()

            self.handle_next_move()
            self.update_frame()

        pygame.quit()