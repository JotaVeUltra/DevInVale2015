import random
from os.path import join
from configparser import ConfigParser

import pygame
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_r, QUIT
from pygame.sprite import GroupSingle, spritecollideany, groupcollide, Group, spritecollide

from sprites import Ship, AsteroidGroup, ShipGroup, ScoreSprite, ExplodingAsteroidsGroup
from constants import TITLE

__author__ = 'julio'


class UserInput:
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.quit = False
        self.fire = False
        self.restart = False

    def reset(self):
        self.__init__()


class Game:
    def __init__(self):
        pygame.init()
        config = ConfigParser()
        config.read('settings.cfg')
        self.width = int(config['VIDEO']['width'])
        self.height = int(config['VIDEO']['height'])
        self.fullscreen = config['VIDEO']['fullscreen'] == 'yes'
        self.player = config['USER']['player']
        self.__config()
        self.__init_screen()
        self.__init_font()
        self.__init_sound()

    def __config(self):
        self.clock = pygame.time.Clock()
        self.elements = {}
        self.input = UserInput()
        self.ship_collides = []
        self.ship_catches = []
        self.newPU = False
        self.score = 0
        self.game_over = False

    def __init_font(self):
        pygame.font.init()
        font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(font_name, 72)
        self.score_font = pygame.font.SysFont(font_name, 38)

    def __init_screen(self):
        resolution = (self.width, self.height)
        flags = 0
        if self.fullscreen:
            flags += pygame.FULLSCREEN
        depth = 9
        self.screen = pygame.display.set_mode(resolution, flags, depth)
        pygame.display.set_caption(TITLE)

    def __init_sound(self):
        self.explosion_sound = pygame.mixer.Sound(join('sfx', 'boom.ogg'))
        self.laser_sound = pygame.mixer.Sound(join('sfx', 'laser.ogg'))
        self.background_sound = pygame.mixer.Sound(join('sfx', 'background.ogg'))

    def update_input(self):
        self.input.reset()
        pressed = pygame.key.get_pressed()

        self.input.up = pressed[K_UP]
        self.input.down = pressed[K_DOWN]
        self.input.left = pressed[K_LEFT]
        self.input.right = pressed[K_RIGHT]
        self.input.fire = pressed[K_SPACE]
        self.input.restart = pressed[K_r]

        for event in pygame.event.get():
            if event.type == QUIT:
                self.input.quit = True
                break
        else:
            self.input.quit = pressed[K_ESCAPE]

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
        self.elements['power-ups'] = Group()
        self.elements['exploding_asteroids'] = ExplodingAsteroidsGroup()
        self.elements['lasers'] = Group()
        self.elements['asteroids'] = AsteroidGroup(join('gfx', 'asteroid.png'), self)
        self.elements['ship'] = ShipGroup(sprite=Ship(join('gfx', 'ship.png'), 48, 48, self))

        while True:
            self.update_input()
            self.update()
            self.draw()
            self.detect_collision()
            if self.input.quit:
                raise SystemExit
            if self.input.restart:
                self.restart()
            self.clock.tick(30)

    def restart(self):
        self.background_sound.stop()
        self.__config()
        self.run()
