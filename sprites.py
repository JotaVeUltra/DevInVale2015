from os.path import join
from random import randrange, choice

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, Group, GroupSingle

import db

__author__ = 'julio'


class Ship(Sprite):
    def __init__(self, img_name, width, height, game):
        super().__init__()

        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(454, 516, width, height)
        self.exploded = False
        self.game = game
        self.cannon_cooldown = 15
        self.poweruptime = 0

    def update(self):
        if not self.exploded:
            if self.game.ship_collides:
                self.exploded = True
                return

            x_move = 0
            y_move = 0
            if self.game.input.up and not self.rect.top <= 0:
                y_move -= 20
            elif self.game.input.down and not self.rect.bottom >= self.game.height:
                y_move += 20
            if self.game.input.left and not self.rect.left <= 0:
                x_move -= 20
            if self.game.input.right and not self.rect.right >= self.game.width:
                x_move += 20
            if self.game.input.fire:
                if self.poweruptime > 0:
                    self.game.laser_sound.play()
                    self.game.elements['lasers'].add(LaserSprite(join('gfx', 'laser.png'), self.rect))
                    self.poweruptime -= 1
                if not self.game.ship_catches:
                    if not self.cannon_cooldown:
                        self.game.laser_sound.play()
                        self.game.elements['lasers'].add(
                            LaserSprite(join('gfx', 'laser.png'), self.rect))
                        self.cannon_cooldown = 6
                else:
                    self.game.ship_catches.pop()
                    self.poweruptime += 75
            self.rect = self.rect.move(x_move, y_move)
            self.cannon_cooldown = self.cannon_cooldown - 1 if self.cannon_cooldown else 0
        else:
            self.groups()[-1].add(AnimatedShip(join('gfx', 'ship_exploded.png'),
                                               self.rect,
                                               3,
                                               self.game))


class ExplodingSprite(Sprite):
    def __init__(self, img_name, rect, sprite_count, game):
        super().__init__()

        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (rect.x, rect.y)
        self.visible_rect = Rect(0, 0, rect.width, rect.width)
        self.explosion_step = 0
        self.game = game
        self.finished = False
        self.sprite_count = sprite_count
        self.game.explosion_sound.play()


class AnimatedShip(ExplodingSprite):
    def update(self):
        self.visible_rect = Rect(self.explosion_step * self.visible_rect.width,
                                 0,
                                 self.visible_rect.width,
                                 self.visible_rect.height)
        self.explosion_step += 1
        if self.explosion_step == self.sprite_count:
            self.groups()[0].add(TextSprite('GAME OVER', self.game))
            self.game.game_over = True
            db.save_score(self.game.player, self.game.score)

            self.kill()


class ShipGroup(GroupSingle):
    def draw(self, surface):
        for sprite in self.sprites():
            params = [sprite.image, sprite.rect]
            try:
                params.append(sprite.visible_rect)
            except AttributeError:
                pass

            self.spritedict[sprite] = surface.blit(*params)
        self.lostsprites = []


class Asteroid(Sprite):
    def __init__(self, img_name, width, height, game):
        super().__init__()
        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(randrange(game.width - width), -100, width, height)
        self.y_speed = randrange(15, 25)
        self.game = game

    def update(self, *args):
        x_move = 0
        y_move = self.y_speed

        self.rect = self.rect.move(x_move, y_move)
        if self.rect.top > self.game.height:
            super().kill()

    def kill(self):
        self.game.elements['exploding_asteroids'].add(AnimatedAsteroid(join('gfx', 'asteroid_exploded.png'),
                                                                       self.rect,
                                                                       4,
                                                                       self.game))
        if self.game.newPU:
            self.game.elements['power-ups'].add(PowerUp(join('gfx', 'PowerUp.png'), self.rect, self.game))
            self.game.newPU = False
        super().kill()


class AnimatedAsteroid(ExplodingSprite):
    def update(self):
        self.visible_rect = Rect(self.explosion_step * self.visible_rect.width,
                                 0,
                                 self.visible_rect.width,
                                 self.visible_rect.height)
        self.explosion_step += 1
        if self.explosion_step == self.sprite_count:
            self.kill()


class ExplodingAsteroidsGroup(Group):
    def draw(self, surface):
        for sprite in self.sprites():
            params = [sprite.image,
                      sprite.rect,
                      sprite.visible_rect]

            self.spritedict[sprite] = surface.blit(*params)
        self.lostsprites = []


class AsteroidGroup(Group):
    def __init__(self, img_name, game, *sprites):
        super().__init__(*sprites)
        self.img_name = img_name
        self.new_asteroid_countdown = 10
        self.game = game

    def update(self, *args):
        self.new_asteroid_countdown -= 1
        if not self.new_asteroid_countdown:
            self.add(Asteroid(self.img_name, 64, 64, self.game))
            self.new_asteroid_countdown = 10

        super().update(*args)


class TextSprite(Sprite):
    def __init__(self, text, game):
        self.image = game.game_font.render(text, 1, (255, 0, 0))
        self.rect = self.image.get_rect().move(335, 250)
        super().__init__()


class ScoreSprite(Sprite):
    def __init__(self, game):
        self.score_text = 'Score: {}'
        self.game = game
        self.score_countdown = 10
        self.update()
        self.rect = self.image.get_rect().move(15, 15)
        super().__init__()

    def update(self, *args):
        if not self.game.game_over:
            if self.score_countdown == 0:
                self.game.score += 1
                self.score_countdown = 10
            else:
                self.score_countdown -= 1
            self.image = self.game.score_font.render(self.score_text.format(self.game.score),
                                                     1,
                                                     (255, 255, 220))


class LaserSprite(Sprite):
    def __init__(self, img_name, rect):
        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(rect.centerx, rect.y, 2, 9)
        super().__init__()

    def update(self):
        self.rect = self.rect.move(0, -10)
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(Sprite):
    def __init__(self, img_name, rect, game):
        self.game = game
        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(rect.centerx, rect.y, 40, 40)
        self.x = choice([-5, 5])
        self.y = choice([-5, 5])
        super().__init__()

    def update(self):
        if self.rect.top <= 0:
            self.y = 5
        if self.rect.bottom >= self.game.height:
            self.y = -5
        if self.rect.left <= 0:
            self.x = 5
        if self.rect.right >= self.game.width:
            self.x = -5
        self.rect = self.rect.move(self.x, self.y)
