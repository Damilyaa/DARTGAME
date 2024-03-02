import pygame
from imageadd import get_res_path


class Button(pygame.sprite.Sprite):

    def __init__(self, loc, image_master, image_covered):
        self.image_master = pygame.image.load(get_res_path(image_master))
        self.image_covered = pygame.image.load(get_res_path(image_covered))
        self.image = self.image_master
        self.loc = loc
        self.rect = self.image.get_rect()
        self.rect.center = self.loc

    def render(self, surface):
        if self.covered():
            self.image = self.image_covered
        else:
            self.image = self.image_master
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def covered(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)