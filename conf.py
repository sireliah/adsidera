
import pygame, sys
from pygame.locals import *

__version__ = 1.0

class Surf(object):

    def __init__(self):
        pygame.init()
        try:
            self.config = open("config", "r+").read().replace('\n', '')
            self.fil = int(self.config)
        except Exception as e:
            #print(e)
            self.fil = 0
        self.mouse_invisible()
        f = pygame.display.list_modes(32)[self.fil]
        self.szer_okna = f[0]
        self.wys_okna = f[1]
        self.pol_szer = int(self.szer_okna/2)
        self.pol_wys = int(self.wys_okna/2)
        self.surface = pygame.display.set_mode((self.szer_okna, self.wys_okna),
                                                FULLSCREEN | HWSURFACE | DOUBLEBUF)
        
    def mouse_visible(self):
        pygame.mouse.set_visible(1)

    def mouse_invisible(self):
        pygame.mouse.set_visible(0)


class Ffonts(object):

    def __init__(self):
        #self.def_font = pygame.font.get_default_font()
        self.def_font = 'data/DejaVuSans.ttf'  #= pygame.font.Font('Helvetica', 30)
        self.czcionka = pygame.font.Font(self.def_font, 23)
        self.czcionka_desc = pygame.font.Font(self.def_font, 17)
        self.czcionka_title = pygame.font.Font(self.def_font, 63)
        self.czcionka_end = pygame.font.Font(self.def_font, 53)
        self.czcionka_subtitle = pygame.font.Font(self.def_font, 19)
        self.czcionka_40 = pygame.font.Font(self.def_font, 33)

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

def endgame():
    print("Game terminated.")
    sys.exit()

WHITE     = (255, 255, 255)
YELLOW    = (255, 255,   0)
BLACK     = (  0,   0,   0)
GRAY      = ( 60,  60,  60)
DARKGRAY  = ( 30,  30,  30)
RED       = (255,   0,   0)
GREEN     = ( 71, 107,   8)
ORANGE    = (255,  36,   0)
ORANGE2   = (255,  140,   0)
BLUE      = (  0,   0, 244)
OCEAN     = (  0,  51, 204)
RUDY      = (204,  51,   0)
IOVIS     = (255, 165,  79)

VERSION = "1.0"
FPS = 40
camx = 0
camy = 0
MARGIN = 50
G = 0.2
RETARDATION = 120

pygame.display.set_caption('Adsidera | v1.0')
s = Surf()
cz = Ffonts()

print(pygame.joystick.get_count())
if pygame.joystick.get_count() > 0:
    ps3 = pygame.joystick.Joystick(0)
    ps3.init()
    print("PS3 pad")
else:
    ps3 = None

