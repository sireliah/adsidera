
import pygame
from pygame.locals import FULLSCREEN, HWSURFACE, DOUBLEBUF


class Fonts(object):

    def __init__(self):
        self.def_font = 'data/DejaVuSans.ttf'
        self.basic = pygame.font.Font(self.def_font, 23)
        self.desc = pygame.font.Font(self.def_font, 17)
        self.title = pygame.font.Font(self.def_font, 63)
        self.end = pygame.font.Font(self.def_font, 53)
        self.subtitle = pygame.font.Font(self.def_font, 19)
        self.bigger = pygame.font.Font(self.def_font, 33)


class Sound(object):

    def __init__(self):
        # self.space = pygame.mixer.Sound('data/power2.ogg')
        self.takeoff = pygame.mixer.Sound('data/takeoff.ogg')
        pygame.mixer.music.load('data/Alex_Mason__The_Minor_Emotion_-_09_-_Only.mp3')

    def play(self, which):
        if which == 'space':
            self.space.play()
        elif which == 'takeoff':
            self.takeoff.play()
        elif which == 'music':
            pygame.mixer.music.play(-1)
        elif which == 'win':
            pygame.mixer.music.load('data/Lobo_Loco_-_06_-_Excalibur_-_Spaceversion_ID_638.mp3')
            pygame.mixer.music.play()


class Sprites(object):

    def __init__(self):
        pygame.sprite.Sprite()
        try:
            self.rocket_image = pygame.image.load("./data/fyndiq_rocket.png").convert_alpha()
            self.rockets = pygame.image.load("data/rocket5.png").convert_alpha()
        except Exception:
            print("Problem loading sprites.")
            raise


class Surface(object):

    def __init__(self):
        pygame.init()
        try:
            self.config = open("config", "r+").read().replace('\n', '')
            self.fil = int(self.config)
        except Exception:
            self.fil = 0
        self.mouse_invisible()
        f = pygame.display.list_modes(32)[self.fil]
        self.window_width = f[0]
        self.window_height = f[1]
        self.pol_szer = int(self.window_width/2)
        self.pol_wys = int(self.window_height/2)
        self.surface = pygame.display.set_mode(
            (self.window_width, self.window_height), FULLSCREEN | HWSURFACE | DOUBLEBUF)

    def mouse_visible(self):
        pygame.mouse.set_visible(1)

    def mouse_invisible(self):
        pygame.mouse.set_visible(0)
