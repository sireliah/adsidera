
import sys
import pygame
from pygame.locals import FULLSCREEN, HWSURFACE, DOUBLEBUF

__version__ = '1.0'


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
        self.surface = pygame.display.set_mode((self.window_width, self.window_height), FULLSCREEN | HWSURFACE | DOUBLEBUF)

    def mouse_visible(self):
        pygame.mouse.set_visible(1)

    def mouse_invisible(self):
        pygame.mouse.set_visible(0)


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
        #self.space = pygame.mixer.Sound('data/power2.ogg')
        self.takeoff = pygame.mixer.Sound('data/takeoff.ogg')

    def play(self, obj):
        if obj == 'space':
            obj = self.space
        elif obj == 'takeoff':
            obj = self.takeoff
        obj.play()


class Colors:

    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    GRAY = (60, 60, 60)
    DARKGRAY = (30, 30, 30)
    RED = (255, 0, 0)
    GREEN = (71, 107, 8)
    ORANGE = (255, 36, 0)
    ORANGE2 = (255, 140, 0)
    BLUE = (0, 0, 244)
    OCEAN = (0, 51, 204)
    GINGER = (204, 51, 0)
    IOVIS = (255, 165, 79)


class GameSettings:

    INIT_CAMX = 0
    INIT_CAMY = 0
    CAMERA_MARGIN = 50
    FPS = 40
    ROCKETS = 3

    RETARDATION = 120
    G_CONSTANT = 0.2


def endgame():
    print("Game terminated.")
    sys.exit()



pygame.display.set_caption('Adsidera | %s' % __version__)

s = Surface()
fonts = Fonts()
