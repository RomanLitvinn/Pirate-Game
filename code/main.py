import sys
import pygame
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        # game attributes
        self.max_level = 5
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # user interface
        self.ui = UI(screen)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.play_music()

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.play_music()

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.play_music()

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.play_music()

    def play_music(self):
        pygame.mixer.music.set_volume(0.1)
        if self.status == "overworld":
            pygame.mixer.music.load("../audio/overworld_music.wav")
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.load("../audio/level_music.wav")
            pygame.mixer.music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mr. Pirate")
pygame.display.set_icon(pygame.image.load("../graphics/character/hat.png").convert_alpha())
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("gray")
    game.run()

    pygame.display.update()
    clock.tick(60)
