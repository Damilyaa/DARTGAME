import os
import csv
import pygame

import TkinterMaster
from tkinter import simpledialog

import imageadd
import colors

class HiScores(object):
    SCORES = {
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

    def __init__(self):
        self.font = pygame.font.Font(imageadd.get_res_path('EraserRegular.ttf'), 18)
        self.scores = []
        for i in range(10):
            self.scores.append({'name': 'SCORE ', 'score': 0})
        self.read()

    def read(self):
        try:
            with open(os.path.join(imageadd.GAME_DIR, 'scores.csv'), 'r') as f:
                reader = csv.reader(f)
                for i, line in enumerate(reader):
                    if i >= 10:
                        break
                    name, score = line
                    self.scores[i]['name'] = name
                    self.scores[i]['score'] = int(score)
        except FileNotFoundError:
            pass

    def write(self):
        with open(os.path.join(imageadd.GAME_DIR, 'scores.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            for score in self.scores:
                writer.writerow((score['name'], score['score']))

    def sort(self):
        self.scores.sort(key=lambda scr: scr['score'], reverse=True)

    def get_name(self):
        root = TkinterMaster.Tk()
        root.withdraw()
        name = simpledialog.askstring('New Record!', ' What is your name?')  # Use simpledialog.askstring
        root.destroy()
        return name

    def check_and_save(self, score):
        if score > self.scores[-1]['score']:
            name = self.get_name()
            self.scores.append({'name': name, 'score': score})
            self.sort()
            self.scores.pop()
            self.write()

    def render(self, surface):
        surface.blit(
            self.font.render('HI-SCORES:', 1, colors.CLR_WHITE), (10, 80)
        )
        for i in range(len(self.scores)):
            score = self.scores[i]
            surface.blit(
                self.font.render(
                    '%s: %s:' % (i + 1, score['name']),
                    1,
                    colors.CLR_WHITE),
                (10, 110 + 40 * i),
            )
            surface.blit(
                self.font.render(
                    '%s' % score['score'],
                    1,
                    colors.CLR_WHITE,
                ),
                (120, 110 + 40 * i)
            )
