
from conf import *

class Menu(object):

    def __init__(self, addd):
        self.addd = addd
        self.s = Surf()
        self.s.mouse_visible()
        self.cz = Ffonts()
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

    def BodiesList(self):
        pygame.draw.rect(s.surface, DARKGRAY, (self.s.pol_szer-400, self.s.pol_wys, 400, len(self.addd.bodies)*22), 0)
        x = 2
        for cialo in self.addd.bodies:
           if cialo.type != 0:
                x = x + 20
                self.star_desc = "[star] "+cialo.name+" "+str(cialo.mass)
                self.planet_desc = "[planet] "+cialo.name+" "+str(cialo.mass)
                star_list = self.cz.czcionka_subtitle.render(self.star_desc, 1, WHITE)
                planet_list = self.cz.czcionka_subtitle.render(self.planet_desc, 1, GRAY)
                if cialo.type == 1:
                    self.s.surface.blit(star_list, (self.s.pol_szer-400, self.s.pol_wys+x))
                else:
                    self.s.surface.blit(planet_list, (self.s.pol_szer-370, self.s.pol_wys+x))

    def BlockStart(self):
        pygame.draw.rect(s.surface, WHITE, self.rect_start, 0)
        self.start = "Start game"
        text = self.cz.czcionka_subtitle.render(self.start, 1, GRAY)
        self.s.surface.blit(text, (self.rect_start.centerx-80, self.rect_start.centery))

    def BlockRandomize(self):
        pygame.draw.rect(s.surface, WHITE, self.rect_rand, 0)
        self.rand = "Randomize"
        text = self.cz.czcionka_subtitle.render(self.rand, 1, GRAY)
        self.s.surface.blit(text, (self.rect_rand.centerx-80, self.rect_rand.centery))

    def block_start_screen(self):
        text1 = "Find and colonize new planets."
        text2 = "To win you have to deploy two colonies and rise them to 3'rd level."
        text3 = "Use [arrows] to steer, [SPACE] to use engine and [ENTER] to release a landing vehicle."

        ren1 = self.cz.czcionka_40.render(text1, 1, WHITE)
        ren2 = self.cz.czcionka_40.render(text2, 1, WHITE)
        ren3 = self.cz.czcionka_40.render(text3, 1, GRAY)

        for i, t in enumerate((ren3, ren2, ren1)):
            self.s.surface.blit(t, (int(self.s.pol_szer/3), int(self.s.pol_wys/(i+2))))
        pygame.draw.rect(s.surface, WHITE, self.rect_start_screen, 0)
        self.start_screen_text = "Start game"
        text = self.cz.czcionka_subtitle.render(self.start_screen_text, 1, GRAY)
        self.s.surface.blit(text, (self.rect_start_screen.centerx-80, self.rect_start_screen.centery))

    def BlockRes(self):
        pygame.draw.rect(s.surface, WHITE, self.rect_res, 0)
        self.res = "Resolution"
        text = self.cz.czcionka_subtitle.render(self.res, 1, GRAY)
        #text.pos = self.rect_quit.position + self.rect_quit.size / 2
        self.s.surface.blit(text, (self.rect_res.centerx-80, self.rect_res.centery))

    def BlockQuit(self):
        pygame.draw.rect(s.surface, WHITE, self.rect_quit, 0)
        self.quit = "Quit"
        text = self.cz.czcionka_subtitle.render(self.quit, 1, GRAY)
        #text.pos = self.rect_quit.position + self.rect_quit.size / 2
        self.s.surface.blit(text, (self.rect_quit.centerx-80, self.rect_quit.centery))

    def Click(self):
        if not self.start_screen:
            if self.rect_start.collidepoint(self.pos):
                #self.menu = False
                self.start_screen = True
            elif self.rect_rand.collidepoint(self.pos):
                self.addd.remove_bodies()
                self.addd.solar_system_bodies()
                self.addd.rand_systems()
                pygame.draw.rect(s.surface, OCEAN, self.rect_quit, 0)
            elif self.rect_quit.collidepoint(self.pos):    
                sys.exit()
            elif self.rect_res.collidepoint(self.pos):
                self.i = self.Switch()
                self.f = self.modes[self.i]
                try:
                    self.config = open("config", "w")
                    self.config.write("%s" % self.i)
                    self.config.close()
                    self.p = Surf()
                    self.s.mouse_visible()
                except IOError as e:
                    print(e)
        else:
            if self.rect_start_screen.collidepoint(self.pos):
                self.menu = False

    def DisplayModes(self):
        self.res_info = pygame.display.Info()
        text = self.cz.czcionka_subtitle.render(str(self.res_info.current_w)+" x "+str(self.res_info.current_h), 1, WHITE)
        self.s.surface.blit(text, (30,30))

    def Version(self):
        text = self.cz.czcionka_subtitle.render(VERSION, 1, WHITE)    
        self.s.surface.blit(text, (self.s.szer_okna-150, self.s.wys_okna-50))
    
    def Switch(self):
        self.i += 1
        if self.i > 5:
            self.i = 0
        return self.i
    
    def Hover(self, objects):
        for r, o in objects:
            if r.collidepoint(self.MousePos()):
                pygame.draw.rect(s.surface, GRAY, r, 0)
                self.text = self.cz.czcionka_subtitle.render(o, 1, WHITE)
                self.s.surface.blit(self.text, (r.centerx-85, r.centery))

    def MousePos(self):
        return pygame.mouse.get_pos()

    def MainScreen(self):
        self.menu = True
        self.start_screen = False
        while self.menu:
            self.Controls()
            s.surface.fill(BLACK)
            if self.start_screen:
                self.show_background()
                self.block_start_screen()
                self.Hover([(self.rect_start_screen, self.start_screen_text)])
            else:
                self.show_background()
                self.show_title()
                self.BodiesList()
                self.BlockStart()
                self.BlockRandomize()
                self.BlockRes()
                self.BlockQuit()
                self.DisplayModes()
                self.Version()
                seq = [(self.rect_start, self.start), (self.rect_rand, self.rand),
                    (self.rect_res, self.res), (self.rect_quit, self.quit)]
                self.Hover(seq)
            pygame.display.update()

    def Controls(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                koniec()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.start_screen and self.menu:
                        self.menu = False
                    self.start_screen = True

                elif event.key == K_ESCAPE:
                    koniec()
                elif event.key == K_SPACE:
                    self.addd.RemoveBodies()
                    self.addd.SolarSystemBodies()
                    self.addd.rand_system()
            elif event.type == MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.Click()
        return self.menu

