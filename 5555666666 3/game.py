import pygame
import mixer

from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE

from imageadd import get_res_path

from dart import Dart
from score import Score
from recordscores import HiScores
from button import Button

from colors import CLR_RED
from colors import CLR_WHITE

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

FPS = 45

IMG_DARTSBOARD = pygame.image.load(get_res_path('dartsboard.png'))
IMG_DARTSBOARD_OFF = pygame.image.load(get_res_path('dartsboard_off.png'))
IMG_CHALKBOARD = pygame.image.load(get_res_path('chalkboard.png'))
IMG_GAMEOVER = pygame.image.load(get_res_path('gameover.png'))

class GameInterruptedError(BaseException):
    pass

class GameEscapedError(BaseException):
    pass

class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.game_surface = pygame.Surface((600, 600), 0, self.screen)
        self.score_surface = pygame.Surface((200, 600), 0, self.screen)
        self.score = Score()
        self.screen.fill((237, 180, 233))
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/bgm.mp3')
        pygame.mixer.music.play(-1)

    def play(self):
        pygame.mouse.set_visible(False)
        for i in range(2):
            turn = Turn(
                i,
                self.screen,
                self.game_surface,
                self.score_surface,
                self.score,
            )
            turn.play()
        recordscores = HiScores()
        recordscores.check_and_save(self.score.total)
        pygame.mixer.music.stop()

class Turn(object):

    def __init__(self, turn_number, screen, game_surface, score_surface, score):
        self.screen = screen
        self.game_surface = game_surface
        self.score_surface = score_surface
        self.score = score
        self.turn_number = turn_number
        self.active_dart = Dart()
        self.darts_remain = 2
        self.dropped_darts = []
        self.font = pygame.font.Font(('images/EraserRegular.ttf'), 32)
        self.splash_font = pygame.font.Font(('images/EraserRegular.ttf'), 52
        )
        self.new_window = None

    def get_turn_name(self):
        if self.turn_number == 1:
            return "Bull's eye"
        else:
            return '%s' % (self.turn_number + 1)

    def play(self):
        clock = pygame.time.Clock()
        self.score_surface.blit(IMG_CHALKBOARD, (0, 0))
        self.score.render(self.score_surface)
        self.game_surface.blit(IMG_DARTSBOARD, (0, 0))
        exit_button1 = Button((-50, -10), 'exit.png', 'exit_covered.png')
        splash1 = self.splash_font.render(
           'Next try:', 1, CLR_RED
        )
        splash2 = self.splash_font.render(
            '%s' % self.get_turn_name(), 1, CLR_RED
        )
        self.game_surface.blit(splash1, (300 - splash1.get_width() / 2, 200))
        self.game_surface.blit(splash2, (300 - splash2.get_width() / 2, 280))
        self.screen.blit(self.game_surface, (0, 0))
        self.screen.blit(self.score_surface, (600, 0))
        pygame.display.update()
        clock.tick(0.8)
        while True:
            clock.tick(FPS)
            self.game_surface.blit(IMG_DARTSBOARD, (0, 0))



            if self.active_dart.dropped:
                self.score.keep(self.turn_number, self.active_dart)
                self.dropped_darts.append(self.active_dart)
                if self.darts_remain > 0:
                    self.active_dart = Dart()
                    self.darts_remain -= 1
                    self.score_surface.blit(IMG_CHALKBOARD, (0, 0))
                    self.score.render(self.score_surface)
                else:
                    break
                if self.turn_number == 2:
                    self.new_window = NewWindow(self.screen)
            for dart in self.dropped_darts:
                dart.render(self.game_surface)
            for e in pygame.event.get():
                if e.type == QUIT:
                    raise GameInterruptedError
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise GameEscapedError
                elif e.type == MOUSEBUTTONDOWN:
                    self.active_dart.drop()
            self.active_dart.handle()
            self.active_dart.move()
            self.active_dart.render(self.game_surface)

            self.game_surface.blit(
                self.font.render('Try: %s' % self.get_turn_name(), 1, CLR_RED),
                (60, 540),
            )

            self.screen.blit(self.game_surface, (0, 0))
            self.screen.blit(self.score_surface, (600, 0))
            pygame.display.update()

class NewWindow(object):
    def __init__(self, screen):
        self.screen = screen
        self.new_screen = pygame.display.set_mode((600, 600), 0, 32)
        self.new_screen.fill((255, 255, 255))
        self.screen.blit(IMG_GAMEOVER, (0, 0))
        pygame.display.set_caption('Game Over')

    def show(self):
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        running = True
        while running:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == QUIT:
                    running = False
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    running = False
            pygame.display.update()
        pygame.display.quit()

def main_screen(screen):
    clock = pygame.time.Clock()
    game_surface = pygame.Surface((600, 600), 0, screen)
    score_surface = pygame.Surface((200, 600), 0, screen)
    start_button = Button((180, 430), 'start.png', 'start_covered.png')
    exit_button = Button((420, 430), 'exit.png', 'exit_covered.png')
    hiscores = HiScores()
    while True:
        clock.tick(FPS)
        screen.fill((255, 255, 255))  # Fill the screen with white color
        game_surface.blit(IMG_DARTSBOARD_OFF, (0, 0))
        score_surface.blit(IMG_CHALKBOARD, (0, 0))
        for e in pygame.event.get():
            if e.type == QUIT:
                raise GameInterruptedError
            elif e.type == MOUSEBUTTONDOWN:
                if start_button.covered():
                    return
                if exit_button.covered():
                    raise GameInterruptedError
        start_button.render(game_surface)
        exit_button.render(game_surface)
        hiscores.render(score_surface)
        screen.blit(game_surface, (0, 0))
        screen.blit(score_surface, (600, 0))
        # update
        pygame.display.update()

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption('darts')

    while True:
        pygame.mouse.set_visible(True)
        try:
            main_screen(screen)
            game = Game(screen)
            game.play()
        except GameEscapedError:
            continue
        except GameInterruptedError:
            break

    pygame.quit()