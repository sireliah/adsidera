
import csv
from datetime import datetime, timedelta
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
    LANDING_VEHICLES = 3
    RETARDATION = 120
    G_CONSTANT = 0.2
    GRAVITY_LIMIT = 150000


def endgame(miliseconds=0):
    if miliseconds:
        time_passed = timedelta(milliseconds=miliseconds)
        print(time_passed)
    print("Game terminated.")
    sys.exit()


def get_elapsed_time(elapsed_mseconds, time_format=''):
    time_passed = timedelta(milliseconds=elapsed_mseconds)
    return time_passed.seconds if time_format == 'seconds' else str(timedelta(seconds=time_passed.seconds))


def write_result(nick, time):
    with open('game_results.txt', 'a') as descriptor:
        descriptor.write("%s|%s\n" % (nick, time))

    return True


def get_timetable():
    # Load best times from the file and sort it.
    data = []
    with open('game_results.txt', 'r') as descriptor:
        reader = csv.reader(descriptor, delimiter="|")
        for row in reader:
            data.append(row)

    return list(sorted(data, key=lambda item: int(item[1])))



s = Surface()
sprites = Sprites()
fonts = Fonts()
sound = Sound()

pygame.display.set_caption('Adsidera | %s' % __version__)
