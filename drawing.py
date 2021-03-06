
import math
import random
import pygame
from conf import s, fonts, Colors, GameSettings


class Trajectory(object):

    """
    Draw the trail left after the body.
    """

    def add_points(self, body, length, count):
        """
        Collect and delete points in which body was in previous frames.
        """
        if length >= 250:
            if body.name == 'rocket':
                body.trail.append((int(body.x), int(body.y)))
            elif count == 5:
                body.trail.append((int(body.x), int(body.y)))

        if len(body.trail) > length:
            del body.trail[0]

    def draw_points(self, trail, camx, camy, length):
        for (counter, (pointx, pointy)) in enumerate(trail):
            if counter > length/1.2:
                pygame.draw.circle(s.surface, Colors.WHITE, (int(pointx-camx), int(pointy-camy)), 2, 2)
            elif counter > length/3:
                pygame.draw.circle(s.surface, (58, 94, 255), (int(pointx-camx), int(pointy-camy)), 2, 2)
            elif counter > length/9:
                pygame.draw.circle(s.surface, (0, 46, 246), (int(pointx-camx), int(pointy-camy)), 2, 2)
            elif counter > length/12:
                pygame.draw.circle(s.surface, (4, 8, 140), (int(pointx-camx), int(pointy-camy)), 2, 2)
            else:
                pygame.draw.circle(s.surface, (2, 5, 70), (int(pointx-camx), int(pointy-camy)), 2, 2)


class Drawing(Trajectory):

    def __init__(self, camx, camy, count, sp, stars):
        self.camx = camx
        self.camy = camy
        self.sp = sp
        self.stars = stars

    def draw_rocket(self, body, camx, camy, sin, cos, imx, imy):
        self.draw_points(body.trail, camx, camy, 200)
        s.surface.blit(self.sp.rocket_image, (int(body.x - imx - camx), int(body.y - imy - camy)))

    def draw_objects(self, body, camx, camy, sin, cos, imx, imy, count, colonies):

        if body.type not in ('star', 'moon',):
            self.add_points(body, 250, count)

        # Make sure that we are drawing objects that are within screen view.
        if (body.x > camx and body.x > camx-s.window_width) and (body.y > camy and body.y > camy-s.window_height):
            # Neither star nor moon.
            if body.type not in ('star', 'moon',):
                self.draw_points(body.trail, camx, camy, 250)

            if body.type == 'star':
                star(body, camx, camy)
            elif body.type == 'planet':
                planet(body, camx, camy)
            elif body.type == 'rocket':
                self.draw_rocket(body, camx, camy, sin, cos, imx, imy)
            else:
                pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)

            colonies.colony_caption(body, camx, camy)

            if body.name not in ('luna', 'rocket'):
                object_caption(int(body.x-camx), int(body.y-camy), body.name)

    def draw_stars(self, camx, camy):
        for starx, stary in self.stars:

            # Make sure to draw only visible start, otherwise this will kill the cpu.
            if (starx > camx and starx > camx-s.window_width) and (stary > camy and stary > camy-s.window_height):
                pygame.draw.circle(s.surface, Colors.WHITE, (int(starx-camx), int(stary-camy)), 1, 1)


def object_caption(x, y, name):
    pygame.draw.line(s.surface, Colors.BLUE, (x+15, y+15), (x+40, y+15), 1)
    pygame.draw.line(s.surface, Colors.BLUE, (x+15, y+15), (x+15, y+25), 1)
    object_caption = fonts.desc.render(str(name), 1, Colors.WHITE)
    s.surface.blit(object_caption, (x+21, y+18))


def planet(body, camx, camy):
    if body.name == 'saturnus':
        pygame.draw.arc(s.surface, Colors.DARKGRAY, (int(body.x-camx-30), int(body.y-camy-15), 60, 25), 0, 3.0, 5)

    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+2, 1)

    if body.name == 'saturnus':
        pygame.draw.arc(s.surface, Colors.GRAY, (int(body.x-camx-30), int(body.y-camy-15), 60, 25), 3.0, 6.0, 5)


def star(body, camx, camy):
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+2, 1)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+5, 1)


def draw_exhaust(exhaust_list):
    """
    When the engine is working, you can see the exhaust flame.
    """
    random_size = random.randint(1, 4)
    random_size1 = random.randint(4, 10)
    random_size2 = random.randint(2, 8)

    if exhaust_list:
        list_x, list_y = exhaust_list[-1]
        pygame.draw.circle(s.surface, Colors.ORANGE2, (int(list_x), int(list_y)), random_size, 1)
        pygame.draw.circle(s.surface, Colors.ORANGE, exhaust_list[-2], random_size1, 2)
        pygame.draw.circle(s.surface, Colors.WHITE, exhaust_list[-3], random_size2, 2)

        del exhaust_list[0]


class HUD(object):

    """
    Game screen static elements like number of rockets, fuel, map, etc.
    """

    def __init__(self, bodies, sp, sin, cos, clock, rockets, landing_vehicles):
        self.bodies = bodies
        self.sp = sp
        self.sin = sin
        self.cos = cos
        self.clock = clock
        self.rockets = rockets
        self.landing_vehicles = landing_vehicles
        self.fps = fonts.basic.render("fps: "+str(self.clock.get_fps()), 1, Colors.OCEAN)

    def main(self, body, camx, camy, naped, cooldown, fuel, gforce, rdist, colonies, fuel_dist):
        self.body = body
        self.camx = camx
        self.camy = camy
        self.cooldown = cooldown
        self.fuel = fuel
        self.rdist = rdist

        s.surface.blit(self.fps, (20, 20))
        if self.body.name == 'rocket':
            text = fonts.basic.render(u"X axis: "+str(int(self.body.x)), 1, Colors.WHITE)
            text2 = fonts.basic.render(u"Y axis: "+str(int(self.body.y)), 1, Colors.WHITE)

            if self.fuel < 100:
                pygame.draw.line(
                    s.surface, Colors.RED,
                    (s.window_width - 300, s.window_height-80),
                    (s.window_width - 295 + (int(self.fuel / 4)), s.window_height - 80),
                    20
                )
            else:
                pygame.draw.line(
                    s.surface, Colors.WHITE,
                    (s.window_width - 300, s.window_height - 80),
                    (s.window_width - 295 + (int(self.fuel / 4)), s.window_height - 80),
                    20
                )

            s.surface.blit(text, (s.window_width-300, s.window_height-140))
            s.surface.blit(text2, (s.window_width-300, s.window_height-120))

            text_fuel = fonts.basic.render(u"Fuel: "+str(self.fuel), 1, Colors.OCEAN)
            s.surface.blit(text_fuel, (s.window_width - 300, s.window_height - 90))
            text_landing_vehicles = fonts.basic.render("Landing vehicles: %s" % self.landing_vehicles, 1, Colors.RED)
            s.surface.blit(text_landing_vehicles, (int(s.window_width - 300), int(s.window_height - 50)))

            self.gravimeter(gforce, fuel_dist)

            colonies.show_col(self.camx, self.camy)

        self.draw_map()

    def gravimeter(self, gforce, fuel_dist):
        """
        Gauge that point to the strongest gravity well.
        """
        angle = math.atan2(gforce[0], gforce[1])
        if math.isnan(angle):
            angle = 0

        pygame.draw.line(
            s.surface,
            Colors.RED,
            (s.window_width - 260 - int(math.sin(angle) * 20), s.window_height - 195 - int(math.cos(angle) * 20)),
            (s.window_width - 260 - int(math.sin(angle) * 32), s.window_height - 193 - int(math.cos(angle) * 32)),
            2
        )

        vert1 = (
            int(self.body.x - self.camx - math.sin(angle) * 90),
            int(self.body.y - self.camy - math.cos(angle) * 90)
        )
        vert2 = (
            int(self.body.x - self.camx - 6 - math.sin(angle) * 50),
            int(self.body.y - self.camy - 6 - math.cos(angle) * 50)
        )
        vert3 = (
            int(self.body.x - self.camx + 6 - math.sin(angle) * 50),
            int(self.body.y - self.camy + 6 - math.cos(angle) * 50)
        )

        pygame.draw.polygon(s.surface, Colors.ORANGE2, (vert1, vert2, vert3), 2)
        pygame.draw.circle(
            s.surface, Colors.DARKGRAY,
            (int(self.body.x-self.camx), int(self.body.y-self.camy)),
            GameSettings.CIRCLE_SIZE,
            1
        )

        if self.rdist < 30:
            pygame.draw.circle(
                s.surface, Colors.GRAY,
                (int(self.body.x-self.camx), int(self.body.y-self.camy)),
                GameSettings.CIRCLE_SIZE,
                2
            )
            pygame.draw.circle(s.surface, Colors.WHITE, (s.window_width-260, s.window_height-193), 33, 1)

        if fuel_dist < 30:
            pygame.draw.circle(
                s.surface, Colors.GREEN,
                (int(self.body.x-self.camx), int(self.body.y-self.camy)),
                GameSettings.CIRCLE_SIZE,
                2
            )

        if self.cooldown < 20:
            pygame.gfxdraw.arc(
                s.surface, s.window_width-260, s.window_height-193, 43, 0, int(self.cooldown*13), Colors.OCEAN
            )
            pygame.gfxdraw.arc(
                s.surface, s.window_width-260, s.window_height-193, 44, 0, int(self.cooldown*13), Colors.OCEAN
            )
            pygame.gfxdraw.arc(
                s.surface, s.window_width-260, s.window_height-193, 46, 0, int(self.cooldown*13), Colors.OCEAN
            )
        else:
            pygame.gfxdraw.arc(
                s.surface, s.window_width-260, s.window_height-193, 43, 0, int(self.cooldown*13), Colors.RED
            )
            pygame.gfxdraw.arc(
                s.surface, s.window_width-260, s.window_height-193, 44, 0, int(self.cooldown*13), Colors.RED
            )

        pygame.draw.circle(s.surface, Colors.DARKGRAY, (s.window_width-260, s.window_height-193), 42, 1)

    def draw_map(self):
        for x in range(0, self.rockets):
            s.surface.blit(self.sp.rockets, (s.window_width-200+40*x, s.window_height-240))

        pygame.draw.rect(s.surface, Colors.WHITE, (0, s.window_height-200, 200, 200), 1)
        map_camera_x = 0
        map_camera_y = 0

        for c in self.bodies:
            if [i for i in self.bodies if i.type == 'rocket']:
                if c.type == 'rocket':
                    map_camera_x = int(c.x / 20 - 100)
                    map_camera_y = int(c.y / 20 - 100)

            else:
                if c.name == 'terra':
                    map_camera_x = int(c.x / 20 - 100)
                    map_camera_y = int(c.y / 20 - 100)
                    if self.rockets > 0:
                        enter_txt = fonts.basic.render(u"Hit ENTER to take off. ", 1, Colors.WHITE)
                        s.surface.blit(enter_txt, (s.window_width-700, s.window_height-500))

            if map_camera_x != 0 and map_camera_y != 0:
                mapx = int(10 + c.x / 20 - map_camera_x)
                mapy = int(s.window_height - 200 + c.y / 20 - map_camera_y)
                if mapx > 0 and mapx < 200 and mapy > s.window_height-200 and mapy < s.window_height:
                    pygame.draw.circle(s.surface, c.color, (mapx, mapy), int(c.size / 4), 0)
