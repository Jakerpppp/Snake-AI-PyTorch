import pygame
import random
import time
import sys
import numpy

class SnakeGameAI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.reset_game()

        self.generation = 0

    def reset_game(self):
        self.game_over = False
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = self._place_food()
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.frame_iteration = 0

    def reset(self):
        self.show_game_over_screen()
        self.generation += 1
        self.reset_game()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render(f'AI Score: {self.score}', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)
        self.screen.blit(game_over_surface, game_over_rect)

        restart_font = pygame.font.SysFont('times new roman', 30)
        restart_surface = restart_font.render(f'Generation: {self.generation}', True, (255, 255, 255))
        restart_rect = restart_surface.get_rect()
        restart_rect.midtop = (self.width / 2, self.height / 2)
        self.screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        time.sleep(1)

    #Main Function
    def run_game(self, action, generation):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            reward = self.move_snake(action)

            # Or End the Game Fully
            if self.game_over:
                return reward, self.game_over, self.score

    def move_snake(self, action):
        self.frame_iteration += 1

        # Straight, right or left depending on agent
        clock_wise = ['RIGHT','DOWN','LEFT','UP']
        index = clock_wise.index(self.direction)

        if numpy.array_equal(action, [1,0,0]):
            new_direction = clock_wise(index) #Straight on
        elif numpy.array_equal(action, [0,1,0]): #Right Turn
            next_index = (index + 1) % 4
            new_direction = clock_wise(next_index)
        else:
            next_index = (index - 1) % 4
            new_direction = clock_wise(next_index)

        self.direction = new_direction

        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_pos[1] += 10
        elif self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        reward = 0
        self.game_over = True
        if self.is_collision() or self.frame_iteration > 100*len(self.snake_body):
            reward = -10
            return reward

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            reward = 10
            self.food_spawn = False
        else:
            self.snake_body.pop()

        self.update_ui()
        self.clock.tick(15)
        return reward

    def _place_food(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.width // 10)) * 10, random.randrange(1, (self.height // 10)) * 10]
        self.food_spawn = True


    def is_collision(self, point=None):
        if point == None:
            point = self.snake_pos
        if point[0] < 0 or point[0] > self.width - 10:
            return True
        if point[1] < 0 or point[1] > self.height - 10:
            return True

        for block in self.snake_body[1:]:
            if point[0] == block[0] and point[1] == block[1]:
                return True

    def update_ui(self):
        self.screen.fill((0, 0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        font = pygame.font.SysFont('times new roman', 20)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

        pygame.display.update()
