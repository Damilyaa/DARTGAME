import math
import random

import pygame
from colors import CLR_WHITE

SECTORS = {
    20: (193, 193),
    1: (193, 60),
    18: (193, 336),
    4: (60, 193),
    13: (122, 193),
    6: (336, 193),
    10: (416, 193),
    15: (193, 416),
    2: (193, 60),
    17: (193, 336),
    3: (60, 193),
    19: (416, 193),
    7: (122, 193),
    16: (336, 193),
    8: (193, 60),
    11: (193, 416),
    14: (193, 336),
    9: (193, 60),
    12: (193, 60),
    5: (193, 193),
}


class Score(object):
    """ Object to help keeping score."""

    def __init__(self):
        self.total = 0
        self.drops = []
        self.font = pygame.font.Font(('images/EraserRegular.ttf'), 24)

    def get_multiplier(self, dist):
        """ Returns multiplier for gotten distant
        """
        if dist < 7 or dist > 78:
            return 0
        elif dist > 43 and dist < 49:
            return 3
        elif dist > 73 and dist < 78:
            return 2
        else:
            return 1

    def keep(self, turn, dart):
        """ Method to keeping score.

        Gets current turn and dart (position), calculates score and
        put it inside.
        """
        center = (300, 300)
        pos = dart.get_pos()
        dist = math.hypot(pos[0] - center[0], pos[1] - center[1])

        angle = math.degrees(math.atan2(center[1] - pos[1], center[0] - pos[0]))
        angle = (angle + 360) % 360
        sector = int(angle / (360 / 20))

        if dist <= 7:
            score = 50
        elif dist <= 78:
            multiplier = self.get_multiplier(dist)
            score = (sector + 1) * multiplier
        else:
            score = 0

        if len(self.drops) == turn:
            self.drops.append([])
        self.drops[turn].append(score)
        self.total += score


    def render(self, surface):
        """ Render scores on gotten surface (surfaca should be 200x600)
        """
        surface.blit(
            self.font.render('Scores:' , 1, CLR_WHITE), (10, 10)
        )
        for i in range(len(self.drops)):
            surface.blit(
                self.font.render('%s: ' % (i + 1), 1, CLR_WHITE),
                (10, 40 + 20 * i),
            )
            for j in range(len(self.drops[i])):
                surface.blit(
                    self.font.render(str(self.drops[i][j]), 1, CLR_WHITE),
                    (50 + 40 * j, 40 + 20 * i),
                )
        surface.blit(
            self.font.render('Total: %s' % self.total, 1, CLR_WHITE),
            (10, 500),
        )



