"""
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more about license you can find in data/coders-crux/license.txt
"""


import pygame
from pygame.locals import *


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


class Menu(object):
    legacy_list = []
    fields = []
    font_size = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    fields_quantity = 0
    background_color = (51, 51, 51)
    text_color = (255, 255, 153)
    selection_color = (153, 102, 255)
    selection_position = 0
    paste_position = (0, 0)
    menu_width = 0
    menu_height = 0

    class Pole(object):
        text = ''
        field = pygame.Surface
        field_rect = pygame.Rect
        selection_rect = pygame.Rect

    def move_menu(self, top, left):
        self.paste_position = (top, left)

    def set_colors(self, text, selection, background):
        self.background_color = background
        self.text_color = text
        self.selection_color = selection

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.selection_position

    def init(self, legacy_list, dest_surface):
        self.legacy_list = legacy_list
        self.dest_surface = dest_surface
        self.fields_quantity = len(self.legacy_list)
        self.create_structure()

    def draw(self, move=0):
        if move:
            self.selection_position += move
            if self.selection_position == -1:
                self.selection_position = self.fields_quantity - 1
            self.selection_position %= self.fields_quantity
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.background_color)
        selection_rect = self.fields[self.selection_position].zaznaczenie_rect
        pygame.draw.rect(menu, self.selection_color, selection_rect)

        for i in xrange(self.fields_quantity):
            menu.blit(self.fields[i].pole, self.fields[i].pole_rect)
        self.dest_surface.blit(menu, self.paste_position)
        return self.selection_position

    def create_structure(self):
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.font_size)
        for i in xrange(self.fields_quantity):
            self.fields.append(self.Pole())
            self.fields[i].tekst = self.legacy_list[i]
            self.fields[i].pole = self.font.render(
                self.fields[i].tekst,
                1,
                self.text_color
            )

            self.fields[i].pole_rect = self.fields[i].pole.get_rect()
            move = int(self.font_size * 0.2)

            height = self.fields[i].pole_rect.height
            self.fields[i].pole_rect.left = move
            self.fields[i].pole_rect.top = move + (move * 2 + height) * i

            width = self.fields[i].pole_rect.width + move * 2
            height = self.fields[i].pole_rect.height + move * 2
            left = self.fields[i].pole_rect.left - move
            top = self.fields[i].pole_rect.top - move

            self.fields[i].zaznaczenie_rect = (left, top, width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.paste_position
        self.paste_position = (x+mx, y+my)


if __name__ == "__main__":
    import sys
    # 0,6671875 and 0,(6) of HD resolution
    surface = pygame.display.set_mode((854, 480))
    surface.fill((51, 51, 51))
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before
    and after *init statement. When you use it before you will move menu from
    center of your surface. When you use it after it will set constant
    coordinates.
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1
    arguments to move selection or nothing. This function will return actual
    position of selection.
    *get_postion will return actual position of seletion. '''
    menu = Menu()  # necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))  # optional
    #menu.set_fontsize(64)  # optional
    #menu.set_font('data/couree.fon')  # optional
    #menu.move_menu(100, 99)  # optional
    menu.init(['Start', 'Options', 'Quit'], surface)  # necessary
    #menu.move_menu(0, 0)  # optional
    menu.draw()  # necessary

    pygame.key.set_repeat(199, 69)  # (delay,interval)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    # here is the Menu class method
                    menu.draw(-1)
                if event.key == K_DOWN:
                    # here is the Menu class method
                    menu.draw(1)
                if event.key == K_RETURN:
                    # here is the Menu class method
                    if menu.get_position() == 2:
                        pygame.display.quit()
                        sys.exit()
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)
