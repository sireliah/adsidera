#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    Adsidera v1.0 Space gravity game
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
from conf import *
from conf import fonts, Colors


class Colony(object):
        
    def __init__(self, planet, resources, level):
        self.planet = planet
        self.resources = resources
        self.level = level


class Colonies(object):

    def __init__(self, rocket_resources):
        self.c = []
        self.rocket_resources = rocket_resources
        #self.c.append(Colony("mars", 0, 0))

    def colony_deployment(self, body1, body2, distance, rocket_resources):
        self.rocket_resources = rocket_resources
        if body1.type == 5 and (body2.type == 2 or body2.type == 4) and body2.name != 'terra':
            if distance < 20:
                # If there is no colony on this planet:
                if not [i for i in self.c if i.planet == body2.name]:
                    self.c.append(Colony(body2.name, 0, 0))
                else:
                    for a in self.c:
                        if a.planet == body2.name:
                            a.resources += 10

    def destroy_colony(self, planet):
        for i, c in enumerate(self.c):
            if c.planet == planet:
                print("Colony %s destroyed!" % c.planet)
                del self.c[i]

    def resources_terra(self, body1, body2, distance):
        if (body1.type == 0 and body2.name == 'terra' and distance < 16):
            return True
        return False

    def load_resources(self):
        return 1

    def show_col(self, kamerax, kameray):
        for i, colony in enumerate(self.c):
            if colony.resources >= 20:
                colony.level = 3
            elif colony.resources >= 10:
                colony.level = 2
            elif colony.resources >= 0:
                colony.level = 1

            if colony.level > 0:
                tekst_colony = fonts.basic.render("%s colony, level: %s" % (colony.planet, colony.level), 2, Colors.GINGER)
                s.surface.blit(tekst_colony, (s.window_width-300, s.window_height/20*i))

    def colony_caption(self, body, camx, camy):
        for col in self.c:
            if col.planet == body.name: 
                pygame.draw.line(s.surface, Colors.ORANGE, (int(body.x-camx+15), int(body.y-camy+12)), (int(body.x-camx+15+col.resources), int(body.y-camy+12)), 4)
                koll = fonts.desc.render("Colony level %s " % col.level, 1, Colors.GINGER)
                s.surface.blit(koll, (int(body.x-camx+23), int(body.y-camy+41)))

