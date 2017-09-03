
import sys
import pygame
from load import Fonts, Sound, Sprites, Surface

__version__ = '1.1'


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
    CIRCLE_SIZE = 50

    ROCKETS = 3
    RETARDATION = 120
    G_CONSTANT = 0.2


def endgame():
    print("Game terminated.")
    sys.exit()


pygame.display.set_caption('Adsidera | %s' % __version__)

s = Surface()
sprites = Sprites()
fonts = Fonts()
sound = Sound()
