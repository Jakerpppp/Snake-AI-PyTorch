import pygame
import random
import time
import sys

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [random.randrange(1, (self.width // 10)) * 10, random.randrange(1, (self.height // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'

            self.move_snake()
            self.check_game_over()
            self.update_ui()
            self.clock.tick(15)

    def move_snake(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_pos[1] += 10
        elif self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.width // 10)) * 10, random.randrange(1, (self.height // 10)) * 10]
        self.food_spawn = True

    def check_game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width - 10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.height - 10:
            self.game_over()

        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over()

    def update_ui(self):
        self.screen.fill((0, 0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        font = pygame.font.SysFont('times new roman', 20)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

        pygame.display.update()

    def game_over(self):
        self.show_game_over_screen()

        # Wait for player to press a key to restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        self.reset_game()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)
        self.screen.blit(game_over_surface, game_over_rect)

        restart_font = pygame.font.SysFont('times new roman', 30)
        restart_surface = restart_font.render('Press any key to play again', True, (255, 255, 255))
        restart_rect = restart_surface.get_rect()
        restart_rect.midtop = (self.width / 2, self.height / 2)
        self.screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        time.sleep(1)

main = SnakeGame()
main.run_game()
