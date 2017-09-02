
import sys
import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, K_RETURN, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN
from conf import (
    __version__, Fonts, Surface, Colors, endgame
)


class Menu(object):

    """
    Rendering menu.
    """

    def __init__(self, addd):
        self.addd = addd
        self.s = Surface()
        self.s.mouse_visible()
        self.fonts = Fonts()
        self.i = 0
        self.modes = pygame.display.list_modes(32)
        self.f = self.modes[0]
        self.blocks()
        self.load_static()

    def blocks(self):
        self.rect_start = Rect(self.s.pol_szer+200, self.s.pol_wys-100, 400, 50)
        self.rect_rand = Rect(self.s.pol_szer+200, self.s.pol_wys-50, 400, 50)
        self.rect_start_screen = Rect(self.s.pol_szer+200, self.s.pol_wys+300, 400, 50)
        self.rect_res = Rect(self.s.pol_szer+200, self.s.pol_wys, 400, 50)
        self.rect_quit = Rect(self.s.pol_szer+200, self.s.pol_wys+50, 400, 50)

    def load_static(self):
        try:
            self.background = pygame.image.load('data/back.png')
            self.background_rect = self.background.get_rect(center=(self.s.pol_szer, self.s.pol_wys))
        except Exception as e:
            print(e)

        try:
            self.title = pygame.image.load('data/title.png')
            self.title_rect = self.background.get_rect(center=(self.s.pol_szer+200, self.s.pol_wys*0.8))
        except Exception as e:
            print(e)

    def show_title(self):
        try:
            self.s.surface.blit(self.title, self.title_rect)
        except Exception as e:
            print(e)

    def show_background(self):
        try:
            self.s.surface.blit(self.background, self.background_rect)
        except Exception as e:
            print(e)

    def bodies_list(self):
        pygame.draw.rect(
            self.s.surface,
            Colors.DARKGRAY,
            (self.s.pol_szer - 400, self.s.pol_wys, 400, len(self.addd.bodies) * 22),
            0
        )
        x = 2
        for body in self.addd.bodies:
            if body.type != 'rocket':
                x = x + 20
                self.star_desc = "[star] " + body.name + " " + str(body.mass)
                self.planet_desc = "[planet] " + body.name + " " + str(body.mass)
                star_list = self.fonts.subtitle.render(self.star_desc, 1, Colors.WHITE)
                planet_list = self.fonts.subtitle.render(self.planet_desc, 1, Colors.GRAY)
                if body.type == 'star':
                    self.s.surface.blit(star_list, (self.s.pol_szer-400, self.s.pol_wys+x))
                else:
                    self.s.surface.blit(planet_list, (self.s.pol_szer-370, self.s.pol_wys+x))

    def block_start(self):
        pygame.draw.rect(self.s.surface, Colors.WHITE, self.rect_start, 0)
        self.start = "Start game"
        text = self.fonts.subtitle.render(self.start, 1, Colors.GRAY)
        self.s.surface.blit(text, (self.rect_start.centerx-80, self.rect_start.centery))

    def block_randomize(self):
        pygame.draw.rect(self.s.surface, Colors.WHITE, self.rect_rand, 0)
        self.rand = "Randomize"
        text = self.fonts.subtitle.render(self.rand, 1, Colors.GRAY)
        self.s.surface.blit(text, (self.rect_rand.centerx-80, self.rect_rand.centery))

    def block_start_screen(self):
        text1 = "Find and colonize new planets."
        text2 = "To win you have to deploy two colonies and rise them to 3'rd level."
        text3 = "Use [arrows] to steer, [SPACE] to use engine and [ENTER] to release a landing vehicle."

        ren1 = self.fonts.bigger.render(text1, 1, Colors.WHITE)
        ren2 = self.fonts.bigger.render(text2, 1, Colors.WHITE)
        ren3 = self.fonts.bigger.render(text3, 1, Colors.GRAY)

        for i, t in enumerate((ren3, ren2, ren1)):
            self.s.surface.blit(t, (int(self.s.pol_szer/3), int(self.s.pol_wys/(i+2))))
        pygame.draw.rect(self.s.surface, Colors.WHITE, self.rect_start_screen, 0)
        self.start_screen_text = "Start game"
        text = self.fonts.subtitle.render(self.start_screen_text, 1, Colors.GRAY)
        self.s.surface.blit(text, (self.rect_start_screen.centerx-80, self.rect_start_screen.centery))

    def block_res(self):
        pygame.draw.rect(self.s.surface, Colors.WHITE, self.rect_res, 0)
        self.res = "Resolution"
        text = self.fonts.subtitle.render(self.res, 1, Colors.GRAY)
        self.s.surface.blit(text, (self.rect_res.centerx-80, self.rect_res.centery))

    def block_quit(self):
        pygame.draw.rect(self.s.surface, Colors.WHITE, self.rect_quit, 0)
        self.quit = "Quit"
        text = self.fonts.subtitle.render(self.quit, 1, Colors.GRAY)
        self.s.surface.blit(text, (self.rect_quit.centerx-80, self.rect_quit.centery))

    def click(self):
        if not self.start_screen:
            if self.rect_start.collidepoint(self.pos):
                self.start_screen = True
            elif self.rect_rand.collidepoint(self.pos):
                self.addd.remove_bodies()
                self.addd.solar_system_bodies()
                self.addd.rand_systems()
                pygame.draw.rect(self.s.surface, Colors.OCEAN, self.rect_quit, 0)
            elif self.rect_quit.collidepoint(self.pos):    
                sys.exit()
            elif self.rect_res.collidepoint(self.pos):
                self.i = self.switch()
                self.f = self.modes[self.i]
                try:
                    self.config = open("config", "w")
                    self.config.write("%s" % self.i)
                    self.config.close()
                    self.p = Surface()
                    self.s.mouse_visible()
                except IOError as e:
                    print(e)
        else:
            if self.rect_start_screen.collidepoint(self.pos):
                self.menu = False

    def display_modes(self):
        self.res_info = pygame.display.Info()
        text = self.fonts.subtitle.render(str(self.res_info.current_w)+" x "+str(self.res_info.current_h), 1, Colors.WHITE)
        self.s.surface.blit(text, (30, 30))

    def version(self):
        text = self.fonts.subtitle.render(__version__, 1, Colors.WHITE)    
        self.s.surface.blit(text, (self.s.window_width-150, self.s.window_height-50))
    
    def switch(self):
        self.i += 1
        if self.i > 5:
            self.i = 0
        return self.i

    def hover(self, objects):
        for r, o in objects:
            if r.collidepoint(self.mouse_pos()):
                pygame.draw.rect(self.s.surface, Colors.GRAY, r, 0)
                self.text = self.fonts.subtitle.render(o, 1, Colors.WHITE)
                self.s.surface.blit(self.text, (r.centerx-85, r.centery))

    def mouse_pos(self):
        return pygame.mouse.get_pos()

    def MainScreen(self):
        self.menu = True
        self.start_screen = False
        while self.menu:
            self.controls()
            self.s.surface.fill(Colors.BLACK)
            if self.start_screen:
                self.show_background()
                self.block_start_screen()
                self.hover([(self.rect_start_screen, self.start_screen_text)])
            else:
                self.show_background()
                self.show_title()
                self.bodies_list()
                self.block_start()
                self.block_randomize()
                self.block_res()
                self.block_quit()
                self.display_modes()
                self.version()
                seq = [
                    (self.rect_start, self.start),
                    (self.rect_rand, self.rand),
                    (self.rect_res, self.res),
                    (self.rect_quit, self.quit)
                ]
                self.hover(seq)
            pygame.display.update()

    def controls(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                endgame()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.start_screen and self.menu:
                        self.menu = False
                    self.start_screen = True

                elif event.key == K_ESCAPE:
                    endgame()
                elif event.key == K_SPACE:
                    self.addd.RemoveBodies()
                    self.addd.SolarSystemBodies()
                    self.addd.rand_system()
            elif event.type == MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.click()
        return self.menu
