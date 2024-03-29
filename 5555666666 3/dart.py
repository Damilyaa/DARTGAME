import random

import pygame

from imageadd import get_res_path


IMG_DART = pygame.image.load(('images/dart.png'))
IMG_DART_DROPPED = pygame.image.load(('images/dart_dropped.png'))
IN_GAME = 0
IN_FLY = 1
DROPPED = 2

FPS = 30
SOUND_DROP = None

def init_mixer():
    global SOUND_DROP
    pygame.mixer.init()
    SOUND_DROP = pygame.mixer.Sound(get_res_path('sounds/hit.mp3'))
class Dart(pygame.sprite.Sprite):

    def __init__(self):
        self.image = IMG_DART
        self.base = (0, 0)
        self.loc = (0., 0.)
        self.radius = 10
        self.path = []
        self.status = IN_GAME
        self.fly_frame = 0

    def make_new_path(self):
        dest = random.choice(
            ((20., 0.), (-20., 0.), (0., 20.), (0., -20.),
             (-16., 12.), (-12., 16.), (16., 12.), (12., 16.),
             (16., -12.), (12., -16.), (-16., -12.), (-12., -16.),)
        )
        length = (dest[0] - self.loc[0], dest[1] - self.loc[1])
        self.path = []
        step = FPS * 3 / 5
        for i in range(int(step)):
            self.path.append(
                (
                    self.loc[0] + length[0] * i / step,
                    self.loc[1] + length[1] * i / step,
                )
            )
        self.path.append(dest)
        self.path.reverse()

    @property
    def dropped(self):
        if self.status == DROPPED:
            return True
        return False

    def drop(self):
        if self.status == IN_GAME:
            self.status = IN_FLY
            if SOUND_DROP is not None:
                SOUND_DROP.play()

    def handle(self):
        if self.status == IN_GAME:
            self.base = pygame.mouse.get_pos()

    def move(self):
        if self.status == IN_GAME:
            if len(self.path) == 0:
                self.make_new_path()
            self.loc = self.path.pop()
        elif self.status == IN_FLY:
            self.fly_frame += 1
            self.image = IMG_DART_DROPPED
            if self.fly_frame == 25:
                self.status = DROPPED

    def render(self, surface):
        self.rect = self.image.get_rect()
        if self.status == IN_GAME:
            self.rect.left = self.base[0] + self.loc[0]
            self.rect.top = self.base[1] + self.loc[1]
        else:
            self.rect.left = self.base[0] + self.loc[0]
            self.rect.bottom = self.base[1] + self.loc[1]
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_pos(self):
        return (self.base[0] + self.loc[0], self.base[1] + self.loc[1])
