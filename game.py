import random
from os.path import join

import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_SPACE
from pygame.locals import K_UP
from pygame.locals import K_r
from pygame.locals import QUIT
from pygame.sprite import GroupSingle, spritecollideany, groupcollide, Group, spritecollide

from db import DB
from sprites import Ship, AsteroidGroup, ShipGroup, ScoreSprite, ExplodingAsteroidsGroup, PowerUpGroup

__author__ = 'julio'


class UserInput:
    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.quit_pressed = False
        self.space_pressed = False

    def reset(self):
        self.__init__()


class Game:
    def __init__(self, *, width=960, height=560, fullscreen=False):
        pygame.init()
        self.__config()
        self.__init_screen(width, height, fullscreen)
        self.__init_font()
        self.__init_sound()
        self.game_over = False
        self.db = DB('game.db')

    def __config(self):
        self.clock = pygame.time.Clock()
        self.elements = {}
        self.input = UserInput()
        self.ship_collides = []
        self.ship_catches = []
        self.newPU = False

    def __init_font(self):
        pygame.font.init()
        font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(font_name, 72)
        self.score_font = pygame.font.SysFont(font_name, 38)

    def __init_screen(self, width, height, fullscreen):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption('DevInVale 2015')
        self.fullscreen = fullscreen
        if self.fullscreen:
            pygame.display.toggle_fullscreen()

    def __init_sound(self):
        pygame.mixer.pre_init(44100, 32, 2, 4096)
        self.explosion_sound = pygame.mixer.Sound(join('sfx', 'boom.ogg'))
        self.laser_sound = pygame.mixer.Sound(join('sfx', 'laser.ogg'))
        self.background_sound = pygame.mixer.Sound(join('sfx', 'background.ogg'))

    def player_input(self):
        self.input.reset()
        pressed_keys = pygame.key.get_pressed()

        if not (pressed_keys[K_UP] and pressed_keys[K_DOWN]):
            if pressed_keys[K_UP]:
                self.input.up_pressed = True
            if pressed_keys[K_DOWN]:
                self.input.down_pressed = True

        if not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
            if pressed_keys[K_LEFT]:
                self.input.left_pressed = True
            if pressed_keys[K_RIGHT]:
                self.input.right_pressed = True

        if pressed_keys[K_SPACE]:
            self.input.space_pressed = True

        if pressed_keys[K_ESCAPE]:
            self.input.quit_pressed = True

        if pressed_keys[K_r]:
            if self.game_over:
                self.restart()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.input.quit_pressed = True

    def update(self):
        for element in self.elements.values():
            element.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for element in self.elements.values():
            element.draw(self.screen)
        pygame.display.update()

    def detect_collision(self):
        if self.elements['ship'].sprite:
            self.ship_collides = spritecollideany(self.elements['ship'].sprite, self.elements['asteroids'])
            self.ship_catches = spritecollide(self.elements['ship'].sprite, self.elements['power-ups'], True)

        if groupcollide(self.elements['lasers'], self.elements['asteroids'], True, True):
            if random.randint(1, 20) == 1:
                self.newPU = True
            self.score_add(50)

    def score_add(self, value):
        self.score += value

    def run(self):
        self.background_sound.set_volume(0.3)
        self.background_sound.play(loops=-1)
        background_filename = join('gfx', 'bg_big.png')
        background_image = pygame.image.load(background_filename).convert()
        self.background = pygame.transform.scale(background_image, (self.width, self.height))

        self.elements['score'] = GroupSingle(ScoreSprite(self))
        self.elements['power-ups'] = PowerUpGroup(join('gfx', 'PowerUp.png'), self)
        self.elements['exploding_asteroids'] = ExplodingAsteroidsGroup()
        self.elements['lasers'] = Group()
        self.elements['asteroids'] = AsteroidGroup(join('gfx', 'asteroid.png'), self)
        self.elements['ship'] = ShipGroup(sprite=Ship(join('gfx', 'ship.png'), 48, 48, self))

        while True:
            self.player_input()
            self.events()
            if self.input.quit_pressed:
                raise SystemExit
            self.update()
            self.draw()
            self.detect_collision()
            self.clock.tick(30)

    def restart(self):
        self.background_sound.stop()
        self.game_over = False
        self.__config()
        self.run()


if __name__ == '__main__':
    game = Game(width=648, height=378)  # (12, 7)
    game.run()