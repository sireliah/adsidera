
from datetime import timedelta
import sys
import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, K_RETURN, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN
from conf import (
    __version__, s, fonts, Surface, Colors, endgame, write_result, get_timetable, get_elapsed_time
)
from libs import pygame_textinput


class Menu(object):

    """
    Rendering menu.
    """

    def __init__(self, addd):
        self.addd = addd
        self.s = Surface()
        s.mouse_visible()
        self.i = 0
        self.modes = pygame.display.list_modes(32)
        self.f = self.modes[0]
        self.blocks()
        self.load_static()

    def blocks(self):
        self.rect_start = Rect(s.half_width+200, s.half_height-100, 400, 50)
        self.rect_rand = Rect(s.half_width+200, s.half_height-50, 400, 50)
        self.rect_start_screen = Rect(s.half_width+200, s.half_height+300, 400, 50)
        self.rect_res = Rect(s.half_width+200, s.half_height, 400, 50)
        self.rect_quit = Rect(s.half_width+200, s.half_height+50, 400, 50)

    def load_static(self):
        self.background = pygame.image.load('data/bg-space-flat-2.png')
        self.background_rect = self.background.get_rect(center=(s.half_width, s.half_height))

        self.background2 = pygame.image.load('data/bg-space-flat.png')
        self.background2_rect = self.background.get_rect(center=(s.half_width, s.half_height))

        self.title = pygame.image.load('data/title.png')
        self.title_rect = self.background.get_rect(center=(s.half_width+200, s.half_height*0.9))

    def show_title(self):
        try:
            s.surface.blit(self.title, self.title_rect)
        except Exception as e:
            print(e)

    def show_background(self, stage=1):
        if stage == 1:
            s.surface.blit(self.background, self.background_rect)
        else:
            s.surface.blit(self.background2, self.background2_rect)

    def bodies_list(self):
        pygame.draw.rect(
            s.surface,
            Colors.DARKGRAY,
            (s.half_width - 400, s.half_height, 400, len(self.addd.bodies) * 22),
            0
        )
        x = 2
        for body in self.addd.bodies:
            if body.type != 'rocket':
                x = x + 20
                self.star_desc = "[star] " + body.name + " " + str(body.mass)
                self.planet_desc = "[planet] " + body.name + " " + str(body.mass)
                star_list = fonts.subtitle.render(self.star_desc, 1, Colors.WHITE)
                planet_list = fonts.subtitle.render(self.planet_desc, 1, Colors.GRAY)
                if body.type == 'star':
                    s.surface.blit(star_list, (s.half_width-400, s.half_height+x))
                else:
                    s.surface.blit(planet_list, (s.half_width-370, s.half_height+x))

    def block_start(self):
        pygame.draw.rect(s.surface, Colors.WHITE, self.rect_start, 0)
        self.start = "Start game"
        text = fonts.subtitle.render(self.start, 1, Colors.GRAY)
        s.surface.blit(text, (self.rect_start.centerx-80, self.rect_start.centery))

    def block_randomize(self):
        pygame.draw.rect(s.surface, Colors.WHITE, self.rect_rand, 0)
        self.rand = "Randomize"
        text = fonts.subtitle.render(self.rand, 1, Colors.GRAY)
        s.surface.blit(text, (self.rect_rand.centerx-80, self.rect_rand.centery))

    def block_start_screen(self):
        text1 = "Find and colonize new planets."
        text2 = "To win you have to deploy 4 colonies."
        text3 = "Try to look for new worlds using the gravimeter arrow."
        text4 = "Use [arrows] to steer, [SPACE] to use engine and [ENTER] to release a landing vehicle."

        ren1 = fonts.title.render(text1, 1, Colors.IOVIS)
        ren2 = fonts.bigger.render(text2, 1, Colors.WHITE)
        ren3 = fonts.bigger.render(text3, 1, Colors.WHITE)
        ren4 = fonts.bigger.render(text4, 1, Colors.WHITE)

        s.surface.blit(ren1, (int(s.half_width / 3), 200))
        s.surface.blit(ren2, (int(s.half_width / 2), 300))
        s.surface.blit(ren3, (int(s.half_width / 2), 350))
        s.surface.blit(ren4, (int(s.half_width / 3), 700))

        pygame.draw.rect(s.surface, Colors.WHITE, self.rect_start_screen, 0)
        self.start_screen_text = "Start game"
        text = fonts.subtitle.render(self.start_screen_text, 1, Colors.GRAY)
        s.surface.blit(text, (self.rect_start_screen.centerx-80, self.rect_start_screen.centery))

    def block_res(self):
        pygame.draw.rect(s.surface, Colors.WHITE, self.rect_res, 0)
        self.res = "Resolution"
        text = fonts.subtitle.render(self.res, 1, Colors.GRAY)
        s.surface.blit(text, (self.rect_res.centerx-80, self.rect_res.centery))

    def block_quit(self):
        pygame.draw.rect(s.surface, Colors.WHITE, self.rect_quit, 0)
        self.quit = "Quit"
        text = fonts.subtitle.render(self.quit, 1, Colors.GRAY)
        s.surface.blit(text, (self.rect_quit.centerx-80, self.rect_quit.centery))

    def click(self):
        if not self.start_screen:
            if self.rect_start.collidepoint(self.pos):
                self.start_screen = True
            elif self.rect_rand.collidepoint(self.pos):
                self.addd.remove_bodies()
                self.addd.solar_system_bodies()
                self.addd.rand_systems()
                pygame.draw.rect(s.surface, Colors.OCEAN, self.rect_quit, 0)
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
                    s.mouse_visible()
                except IOError as e:
                    print(e)
        else:
            if self.rect_start_screen.collidepoint(self.pos):
                self.menu = False

    def display_modes(self):
        self.res_info = pygame.display.Info()
        text = fonts.subtitle.render(
            str(self.res_info.current_w) + " x " + str(self.res_info.current_h), 1, Colors.WHITE)
        s.surface.blit(text, (30, 30))

    def version(self):
        text = fonts.subtitle.render(__version__, 1, Colors.WHITE)
        s.surface.blit(text, (s.window_width-150, s.window_height-50))

    def switch(self):
        self.i += 1
        if self.i > 12:
            self.i = 0
        return self.i

    def hover(self, objects):
        for r, o in objects:
            if r.collidepoint(self.mouse_pos()):
                pygame.draw.rect(s.surface, Colors.GRAY, r, 0)
                self.text = fonts.subtitle.render(o, 1, Colors.WHITE)
                s.surface.blit(self.text, (r.centerx-85, r.centery))

    def mouse_pos(self):
        return pygame.mouse.get_pos()

    def MainScreen(self):
        self.menu = True
        self.start_screen = False
        while self.menu:
            self.controls()
            s.surface.fill(Colors.BLACK)
            if self.start_screen:
                self.show_background(stage=2)
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


def show_timetable(timetable):
    rect_timetable = Rect(450, s.half_height - 200, 900, 800)
    pygame.draw.rect(s.surface, Colors.GRAY, rect_timetable, 0)

    counter = 0
    distancer = 0
    for row in timetable:
        counter += 1
        distancer += 40

        game_time = timedelta(seconds=int(row[1]))
        timetable_numbers = fonts.basic.render("%s." % counter, 1, Colors.IOVIS)
        timetable_time = fonts.basic.render("%s" % game_time, 1, Colors.YELLOW)
        timetable_nick = fonts.basic.render("%s" % row[0], 1, Colors.WHITE)
        s.surface.blit(timetable_numbers, (480, s.half_height - 200 + distancer))
        s.surface.blit(timetable_time, (540, s.half_height - 200 + distancer))
        s.surface.blit(timetable_nick, (720, s.half_height - 200 + distancer))


def show_victory_screen(elapsed_mseconds):
    textinput = pygame_textinput.TextInput(text_color=Colors.GRAY)
    nick = None
    written = False
    timetable = []

    while True:
        background = pygame.image.load("data/rocket_bg.png")
        background_rect = background.get_rect(center=(s.half_width, s.half_height))
        s.surface.blit(background, background_rect)

        events = pygame.event.get()

        if textinput.update(events):
            nick = textinput.get_text()

        for event in events:
            if event.type == pygame.QUIT:
                endgame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    endgame()
                elif event.key == K_RETURN:
                    if not written:
                        written = write_result(nick, get_elapsed_time(elapsed_mseconds, time_format='seconds'))
                        timetable = get_timetable()

        gameover = fonts.title.render("You won!", 1, Colors.WHITE)
        your_time = fonts.end.render("Your time: %s" % get_elapsed_time(elapsed_mseconds), 1, Colors.YELLOW)

        s.surface.blit(gameover, (200, 100))
        s.surface.blit(your_time, (200, 200))

        if timetable:
            show_timetable(timetable)

        else:
            type_name = fonts.basic.render("Please type your name and press ENTER:", 1, Colors.WHITE)
            small_text = fonts.desc.render("We support Ünicode!", 1, Colors.WHITE)
            s.surface.blit(type_name, (200, 300))
            s.surface.blit(small_text, (200, 340))
            s.surface.blit(textinput.get_surface(), (200, 380))

        pygame.display.update()
