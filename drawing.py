#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    Adsidera v0.4 Space gravity game
    for more info, please visit http://sourceforge.net/projects/adsidera/
 
    Copyright (C) 2013 Piotr Gołąb

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import math
import random
from numpy import mean
from conf import *

class Sprites(object):
        
    def __init__(self):
        pygame.sprite.Sprite()
        try:
            self.image = pygame.image.load("./data/rakieta.png").convert_alpha()
            self.rockets = pygame.image.load("data/rakieta5.png").convert_alpha()
        except:
            print("Problem loading sprites.")
            raise

class Traj(object):

    def add_points(self, body, length, count):
        if length >= 250:
            if body.name == 'rakieta':
                body.trail.append((int(body.x), int(body.y)))
            elif count == 5:
                body.trail.append((int(body.x), int(body.y)))

        if len(body.trail) > length:
            del body.trail[0]

    def draw_points(self, trail, camx, camy, length):
        for (licznik, (punktx, punkty)) in enumerate(trail):
            if licznik > length/1.2:
                pygame.draw.circle(s.surface, WHITE, (int(punktx-camx), int(punkty-camy)), 2, 2)
            elif licznik > length/3:
                pygame.draw.circle(s.surface, (58, 94, 255), (int(punktx-camx), int(punkty-camy)), 2, 2)
            elif licznik > length/9:
                pygame.draw.circle(s.surface, (0, 46, 246), (int(punktx-camx), int(punkty-camy)), 2, 2)
            elif licznik > length/12:
                pygame.draw.circle(s.surface, (4, 8, 140), (int(punktx-camx), int(punkty-camy)), 2, 2)
            else:
                pygame.draw.circle(s.surface, (2, 5, 70), (int(punktx-camx), int(punkty-camy)), 2, 2)


class Drawing(Traj):

     #   (gwiazdy, sin, cos, camx, camy, lista, sp, k, imx, imy, licz):
    def __init__(self, camx, camy, count, sp, stars):
        Traj.__init__(self)
        self.camx = camx
        self.camy = camy
        self.sp = sp
        self.stars = stars
    
    def draw_rocket(self, body, camx, camy, sin, cos, imx, imy):
        self.draw_points(body.trail, camx, camy, 200)
        #Rakieta(int(body.x-camx), int(body.y-camy), sin, cos)
        s.surface.blit(self.sp.image, (int(body.x-imx-camx), int(body.y-imy-camy)))

    def draw_objects(self, body, camx, camy, sin, cos, imx, imy, count, colonies):

        if body.type != 1 and body.type != 3 and body.type != 6:
            self.add_points(body, 250, count)

        # Make sure that we are drawing objects that are within screen view.
        if (body.x > camx and body.x > camx-s.szer_okna) and (body.y > camy and body.y > camy-s.wys_okna):
            # Neither star nor moon.
            if body.type != 1 and body.type != 3 and body.type != 6:
                self.draw_points(body.trail, camx, camy, 250)

            if body.type == 1:
                star(body, camx, camy)
            elif body.type == 2:
                planet(body, camx, camy)
            #elif body.type == 6:
            #    pass
            elif body.name == 'rakieta':
                self.draw_rocket(body, camx, camy, sin, cos, imx, imy)
            else: 
                pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)

            colonies.colony_caption(body, camx, camy)

            if body.name != 'luna' and body.name != 'rakieta' and body.type != 6:
                object_caption(int(body.x-camx), int(body.y-camy), body.name)
            if body.type == 6:
                an = math.atan2(body.velocityx, body.velocityy)
                if not math.isnan(an):
                    an = an - math.pi
                    x = math.sin(an)
                    y = math.cos(an)
                    #print(body.name, x, y)
                    """
                    WOW
                    pygame.draw.line(s.surface, RED,
                                     (body.x-camx, body.y-camy),
                                     ((body.x-x-camx)*2, (body.y-y-camy)*2),
                                     1)
                    """
                    pygame.draw.line(s.surface, RED,
                                     (int(body.x-camx), int(body.y-camy)),
                                     (int(body.x-camx-(x*100)), int(body.y-camy-(y*100))),
                                     1)

    def draw_stars(self, camx, camy):
        for starx, stary in self.stars:
            if (starx > camx and starx > camx-s.szer_okna) and (stary > camy and stary > camy-s.wys_okna):
                pygame.draw.circle(s.surface, WHITE, (int(starx-camx), int(stary-camy)), 1, 1)


def object_caption(x, y, name):
    pygame.draw.line(s.surface, BLUE, (x+15, y+15), (x+40, y+15), 1)
    pygame.draw.line(s.surface, BLUE, (x+15, y+15), (x+15, y+25), 1)
    object_caption = cz.czcionka_desc.render(str(name), 1, WHITE)
    s.surface.blit(object_caption, (x+21, y+18))
    #koordynaty = cz.czcionka_desc.render("x: "+str(x)+" y: "+str(y), 1, BLUE)
        #s.surface.blit(koordynaty, (x+22, y+30))


def planet(body, camx, camy):
    if body.name == 'saturnus':
        pygame.draw.arc(s.surface, DARKGRAY, (int(body.x-camx-30), int(body.y-camy-15), 60, 25), 0, 3.0, 5)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+2, 1)
    if body.name == 'saturnus':
        pygame.draw.arc(s.surface, GRAY, (int(body.x-camx-30), int(body.y-camy-15), 60, 25), 3.0, 6.0, 5)
        

def star(body, camx, camy):
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size, 0)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+2, 1)
    pygame.draw.circle(s.surface, body.color, (int(body.x-camx), int(body.y-camy)), body.size+5, 1)
    """
    i = mass*100
    while i > size:
        #print(i)
        i = i /2
        #print(i)
        #if i > size:
        pygame.draw.circle(s.surface, planeta_kolor, (starx, stary), int(i), 1)
    """
        


"""
def Rakieta(x, y, sin, cos):
        s = 8 * sin
        c = 8 * cos
    punkt = (int(x-s/3), int(y-c/3))
    pygame.draw.line(s.surface, (32, 104, 235), punkt, punkt, 3)
        pygame.draw.line(s.surface, ORANGE, (x-s/30, y-c/30), (x+s, y+c), 2)
"""

def draw_trail(trail_list):
    los = random.randint(1, 4)
    los1 = random.randint(4, 10)
    los2 = random.randint(2, 8)
    if trail_list:
        listax, listay = trail_list[-1]
        pygame.draw.circle(s.surface, ORANGE2, (int(listax), int(listay)), los, 1)
        pygame.draw.circle(s.surface, ORANGE, trail_list[-2], los1, 2)
        pygame.draw.circle(s.surface, RED, trail_list[-3], los2, 2)

        del trail_list[0]

def stars():
    stars = []
    for a in range(5000):
        wsp1 = random.randint(-8000, 8000)
        wsp2 = random.randint(-8000, 8000)
        stars.append((wsp1, wsp2))
    return stars



class HUD(object):
        
    def __init__(self, bodies, sp, sin, cos, clock, rockets, landing_vehicles):
        self.bodies = bodies
        self.sp = sp
        self.sin = sin
        self.cos = cos
        self.s = 8 * self.sin
        self.c = 8 * self.cos
        self.clock = clock
        self.rockets = rockets
        self.landing_vehicles = landing_vehicles
        self.fps = cz.czcionka.render("fps: "+str(self.clock.get_fps()), 1, OCEAN)
            
    def main(self, body, camx, camy, naped, cooldown, fuel, gforce, rdist, colonies, fuel_dist):
        self.body = body
        self.camx = camx
        self.camy = camy
        self.sz = s.szer_okna
        self.wys = s.wys_okna
        self.cooldown = cooldown
        self.fuel = fuel
        self.rdist = rdist

        s.surface.blit(self.fps, (20, 20))
        if self.body.name == 'rakieta':
            tekst = cz.czcionka.render(u"X axis: "+str(int(self.body.x)), 1, WHITE)
            tekst2 = cz.czcionka.render(u"Y axis: "+str(int(self.body.y)), 1, WHITE)
            if self.fuel < 100:
                pygame.draw.line(s.surface, RED, (self.sz-300, self.wys-80), (self.sz-295+(int(self.fuel/4)), self.wys-80), 20) 
            else: 
                pygame.draw.line(s.surface, WHITE, (self.sz-300, self.wys-80), (self.sz-295+(int(self.fuel/4)), self.wys-80), 20)
            s.surface.blit(tekst, (self.sz-300, self.wys-140))
            s.surface.blit(tekst2, (self.sz-300, self.wys-120))
            tekst_fuel = cz.czcionka.render(u"Fuel: "+str(self.fuel), 1, OCEAN)
            s.surface.blit(tekst_fuel, (self.sz-300, self.wys-90))
            text_landing_vehicles = cz.czcionka.render("Landing vehicles: %s" % self.landing_vehicles, 1, RED)
            s.surface.blit(text_landing_vehicles, (int(s.szer_okna-300), int(s.wys_okna-50)))
            self.Gravimeter(gforce, fuel_dist)

            colonies.show_col(self.camx, self.camy)
        self.Map()

    def Gravimeter(self, gforce, fuel_dist):
        angle = math.atan2(gforce[0], gforce[1])
        if math.isnan(angle):
            angle = 0
        pygame.draw.line(s.surface, RED, (self.sz-260-int(math.sin(angle)*20), self.wys-195-int(math.cos(angle)*20)),
                         (self.sz-260-int(math.sin(angle)*32), self.wys-193-int(math.cos(angle)*32)),
                         2)
    
        z1 = (int(self.body.x-self.camx-math.sin(angle)*45), int(self.body.y-self.camy-math.cos(angle)*45))
        z2 = (int(self.body.x-self.camx-3-math.sin(angle)*30), int(self.body.y-self.camy-3-math.cos(angle)*30))
        z3 = (int(self.body.x-self.camx+6-math.sin(angle)*30), int(self.body.y-self.camy+6-math.cos(angle)*30))
        pygame.draw.polygon(s.surface, GRAY, (z1, z2, z3), 2)
        pygame.draw.circle(s.surface, DARKGRAY, (int(self.body.x-self.camx), int(self.body.y-self.camy)), 30, 1)
        if self.rdist < 30:
            pygame.draw.circle(s.surface, GRAY, (int(self.body.x-self.camx), int(self.body.y-self.camy)), 30, 2)
            pygame.draw.circle(s.surface, WHITE, (self.sz-260, self.wys-193), 33, 1)
        if fuel_dist < 30:
            pygame.draw.circle(s.surface, GREEN, (int(self.body.x-self.camx), int(self.body.y-self.camy)), 30, 2)
        if self.cooldown < 20:
            pygame.gfxdraw.arc(s.surface, self.sz-260, self.wys-193, 43, 0, int(self.cooldown*13), OCEAN)
            pygame.gfxdraw.arc(s.surface, self.sz-260, self.wys-193, 44, 0, int(self.cooldown*13), OCEAN)
            pygame.gfxdraw.arc(s.surface, self.sz-260, self.wys-193, 46, 0, int(self.cooldown*13), OCEAN)
        else: 
            pygame.gfxdraw.arc(s.surface, self.sz-260, self.wys-193, 43, 0, int(self.cooldown*13), RED)
            pygame.gfxdraw.arc(s.surface, self.sz-260, self.wys-193, 44, 0, int(self.cooldown*13), RED)
        pygame.draw.circle(s.surface, DARKGRAY, (self.sz-260, self.wys-193), 42, 1)

    #@profile
    def Map(self):
        for x in range(0, self.rockets):
            #pygame.draw.polygon(s.surface, WHITE, ((self.sz-150+20*x, self.wys-150), (self.sz-155+20*x, self.wys-220), (self.sz-160+20*x, self.wys-150)), 1)
            s.surface.blit(self.sp.rockets, (self.sz-200+40*x, self.wys-240))
    
        pygame.draw.rect(s.surface, WHITE, (0, self.wys-200, 200, 200), 1)
        kam_mapx = 0
        kam_mapy = 0
        for c in self.bodies:
            if c.type is not 6:
                if [i for i in self.bodies if i.type == 0]:
                    if c.type == 0:
                        kam_mapx = int(c.x/20-100)
                        kam_mapy = int(c.y/20-100)
        
                else:
                    if c.name == 'terra':
                        kam_mapx = int(c.x/20-100)
                        kam_mapy = int(c.y/20-100)
                        if self.rockets > 0:
                            enter_txt = cz.czcionka.render(u"Hit ENTER to take off. ", 1, WHITE)
                            s.surface.blit(enter_txt, (self.sz-700, self.wys-500))
                    
                if kam_mapx != 0 and kam_mapy != 0:
                    mapx = int(10+c.x/20-kam_mapx)
                    mapy = int(self.wys-200+c.y/20-kam_mapy)
                    if mapx > 0 and mapx < 200 and mapy > self.wys-200 and mapy < self.wys:
                        pygame.draw.circle(s.surface, c.color, (mapx, mapy), int(c.size/4), 0)

