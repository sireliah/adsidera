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
import pygame
import time
import math
import random
from numpy import mean
from pygame import joystick
from pygame import gfxdraw
from pygame.locals import *

from bodies import Body, BodiesCreator

from mainmenu import Menu

from conf import fonts, s, Colors, Sound, GameSettings, endgame
from colonies import Colonies
from drawing import Drawing, Sprites, HUD, draw_trail
from planet_names import PLANET_NAMES, STAR_NAMES


class Mainloop(object):

    def __init__(self, camx, camy):
        self.camx, self.camy = camx, camy
        self.rocket_angle = math.radians(math.pi/2)
        self.addd = BodiesCreator(STAR_NAMES, PLANET_NAMES)
        self.bodies = self.addd.rand_systems()
        self.clock = pygame.time.Clock()
        mm = Menu(self.addd)
        mm.MainScreen()
        s.mouse_invisible()
        self.sound = Sound()
        self.enter = 0
        self.rdist = 100
        self.rocket_circle = 100
        self.rocket_resources = 100
        self.count = 0
        self.rockets = GameSettings.ROCKETS
        self.thrust = 1
        self.gforce = (0, 0)
        self.trail_list = []
        self.lander_dist = 0
        self.landing_vehicle_lock = False
        self.landing_vehicles = 3
        self.llx, self.lly = [], []
        self.cooldown = 0
        self.fuel = 1000
        self.fuel_dist = 0
        self.vectorx, self.vectory = 1, 1
        self.landerx, self.landery = 0, 0
        self.imx, self.imy = 6, 16
        self.thrl, self.thrr = 0, 0
        self.sp = Sprites()
        self.image_orig = self.sp.image.copy()
        self.colonies = Colonies(self.rocket_resources)
        self.d = Drawing(self.camx, self.camy, self.count, self.sp, BodiesCreator.generate_stars())

    def play(self):
        while True:
            self.counter()
            self.victory_conditions()
            self.landing_vehicle_lock = False
            s.surface.fill(Colors.BLACK)
            self.sin = math.sin(self.rocket_angle)
            self.cos = math.cos(self.rocket_angle)
            self.hud = HUD(self.bodies, self.sp, self.sin, self.cos, self.clock, self.rockets, self.landing_vehicles)
            self.events()
            self.bodies_interactions()

            oldrect = self.sp.image.get_rect()
            self.sp.image = pygame.transform.rotozoom(self.image_orig, int(math.degrees(self.rocket_angle)), 1)
            newrect = self.sp.image.get_rect()
            self.imx += newrect.centerx - oldrect.centerx
            self.imy += newrect.centery - oldrect.centery

            self.rockets_available()
            self.gforce = (mean(self.llx), mean(self.lly))
            self.addd.comets()
            self.d.draw_stars(self.camx, self.camy)
            del self.llx[:]
            del self.lly[:]
            self.clock.tick_busy_loop(GameSettings.FPS)
            pygame.display.flip()

    def bodies_physics(self, body):
        if [i for i in self.bodies if i.name == 'rocket']:

            if body.name == 'rocket':
                body.x += body.velocityx + self.vectorx / GameSettings.RETARDATION
                body.y += body.velocityy + self.vectory / GameSettings.RETARDATION
                self.camera(body, center_on='rocket')

            elif body.type == 5:
                lander_angle = math.atan2(self.landerx, self.landery)
                if self.lander_dist < 200:
                    sx = body.velocityx - (math.sin(lander_angle) / 2)
                    sy = body.velocityy - (math.cos(lander_angle) / 2)
                else:
                    sx = body.velocityx / GameSettings.RETARDATION
                    sy = body.velocityy / GameSettings.RETARDATION
                body.x += sx
                body.y += sy
            elif body.type == 6:
                pass
            else:
                body.x += body.velocityx / GameSettings.RETARDATION
                body.y += body.velocityy / GameSettings.RETARDATION

        else:
            body.x += body.velocityx / GameSettings.RETARDATION
            body.y += body.velocityy / GameSettings.RETARDATION
            self.camera(body, center_on='terra')

    def bodies_interactions(self):

        for body1 in self.bodies:
            self.control_pressed(body1)
            self.hud.main(
                body1,
                self.camx,
                self.camy,
                self.thrust,
                self.cooldown,
                self.fuel,
                self.gforce,
                self.rdist,
                self.colonies,
                self.fuel_dist
            )
            self.rocket_dynamics()
            self.bodies_physics(body1)
            self.d.draw_objects(
                body1,
                self.camx,
                self.camy,
                self.sin,
                self.cos,
                self.imx,
                self.imy,
                self.count,
                self.colonies
            )

            for body2 in self.bodies:
                if body1 != body2:

                    # Distance between two bodies.
                    distance = math.sqrt(
                        (body1.x - body2.x) ** 2 + (body1.y - body2.y) ** 2
                    )

                    #self.col = Colony(body1, body2, distance, self.rocket_circle)
                    self.collisions(body1, body2, distance)
                    self.fuel_out(body1, body2, distance)

                    if distance < 15:
                        distance = 14
                    if distance < 150000:

                        """
                        Newton's law of universal gravitation.
                        """

                        # Calculate the gravitational force between two bodies.
                        F = GameSettings.G_CONSTANT * (body1.mass * body2.mass / (distance * distance))

                        # Calculate the acceleration of the body.
                        a = F / body1.mass

                        # Calculate velocity components.
                        componentx = (a * (body1.x - body2.x)) / distance 
                        componenty = (a * (body1.y - body2.y)) / distance

                        if body1.name == 'rocket' or body2.name == 'rocket':
                            self.llx.append(componentx)
                            self.lly.append(componenty)

                            if body2.type == 2:
                                self.fuel_dist = distance
                                if self.fuel_dist < 30:
                                    self.load_fuel()
                                    pygame.draw.circle(
                                        s.surface, Colors.GREEN,
                                        (int(body1.x-self.camx), int(body1.y-self.camy)),
                                        30, 2
                                    )

                        if 'landing vehicle' in body1.name:
                            if body2.type == 2:
                                self.lander_dist = distance
                                if distance < 200:
                                    self.landerx = componentx
                                    self.landery = componenty
                                    if distance < 17:
                                        self.colonies.colony_deployment(body1, body2, distance, self.rocket_resources)
                                        self.del_body(body1.name)
                            elif body2.type == 0:
                                # Distance from rocket to landing vehicle
                                self.rdist = distance
                        if not [i for i in self.bodies if i.name == 'rocket']:
                            if body1.name == 'terra':
                                if body2.name == 'sol':
                                    self.tvx = componentx
                                    self.tvy = componenty

                    # Subtract velocity components.
                    if distance < 1500:
                        body1.velocityx -= componentx
                        body1.velocityy -= componenty

                    # Remove far objects.
                    self.distant_bodies_remover(body1, body2, distance)

                    # Load resources from Terra
                    if self.colonies.resources_terra(body1, body2, distance):
                        self.landing_vehicles += 1
                    if self.landing_vehicles > 3:
                        self.landing_vehicles = 3

    def camera(self, body, center_on=''):
        if body.name == center_on:
            if (self.camx + s.pol_szer) - body.x > GameSettings.CAMERA_MARGIN:
                self.camx = body.x + GameSettings.CAMERA_MARGIN - s.pol_szer
            elif body.x - (self.camx + s.pol_szer) > GameSettings.CAMERA_MARGIN:
                self.camx = body.x - GameSettings.CAMERA_MARGIN - s.pol_szer
            if (self.camy + s.pol_wys) - body.y > GameSettings.CAMERA_MARGIN:
                self.camy = body.y + GameSettings.CAMERA_MARGIN - s.pol_wys
            elif body.y - (self.camy + s.pol_wys) > GameSettings.CAMERA_MARGIN:
                self.camy = body.y - GameSettings.CAMERA_MARGIN - s.pol_wys

    def events(self):
        for event in pygame.event.get():
            for body in self.bodies:
                if body.name == 'terra':
                    self.zx = body.x
                    self.zy = body.y

                if event.type == QUIT:
                    endgame()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Game terminated.")
                        endgame()

                    elif event.key == K_c and body.name == 'rocket':
                        self.thrust = self.thrust - 0.1
                    elif event.key == K_RETURN and body.name == 'terra':
                        if not [i for i in self.bodies if i.name == 'rocket']:
                            direction = math.atan2(self.tvy, self.tvx)
                            vx = math.cos(direction)
                            vy = math.sin(direction)
                            self.bodies.insert(0, Body('rocket', 0, Colors.WHITE, self.zx+1, self.zy+1, vx*6, vy*6, 1, 1, (0,0)
                                                  )
                                           )
                            self.fuel = 1000
                            self.landing_vehicles = 3
                            self.sound.play('takeoff')
                            self.vectorx = 0
                            self.vectory = 0
                    elif event.key == K_RETURN:
                        if body.name == 'rocket':
                            rx = body.x
                            ry = body.y
                            lv = [i for i in self.bodies if "landing vehicle" in i.name]
                            if lv:
                                #self.rdist = math.sqrt((rx - lx)**2 + (ry - ly)**2)
                                if self.rdist < 30:
                                    self.rocket_circle += 10
                                    self.rdist = 100
                                    self.del_body(lv[0].name)
                                    self.landing_vehicles += 1
                                    self.landing_vehicle_lock = True

                            if self.landing_vehicles > 0 and not self.landing_vehicle_lock:
                                self.bodies.insert(
                                    0,
                                    Body('landing vehicle %s' % random.randint(1, 100),
                                         5, Colors.GINGER,
                                         body.x, body.y,
                                         body.velocityx + self.sin * 30,
                                         body.velocityy + self.cos * 30,
                                         1, 2,
                                         (0,0)
                                    )
                                )
                                self.rocket_circle -= 10
                                self.landing_vehicles -= 1
                                lx = body.x
                                ly = body.y
                                self.sound.play('takeoff')
                                self.landing_vehicle_lock = True
                        elif "landing vehicle" in body.name:
                            lx = body.x
                            ly = body.y

    def rocket_dynamics(self):
        if self.rocket_angle > math.radians(360):
            self.rocket_angle = math.radians(0)
        elif self.rocket_angle < math.radians(0):
            self.rocket_angle = math.radians(360)
        if self.thrust > 0.1:
            self.thrust = self.thrust - 0.6
        if self.thrust < 0.01:
            self.thrust = 0.01
        if self.vectorx > 1:
            self.vectorx - 0.1
        if self.vectory < 1:
            self.vectory + 0.1
        if self.cooldown > 0:
            self.cooldown -= 0.005

    def control_pressed(self, body):
        keys = pygame.key.get_pressed()
        if body.name == 'rocket':
            if keys[K_RIGHT]:
                self.rcs_thruster(body.x, body.y, "p")
                self.rocket_angle = self.rocket_angle - math.radians(4)
            if keys[K_LEFT]:
                self.rcs_thruster(body.x, body.y, "l")
                self.rocket_angle = self.rocket_angle + math.radians(4)
            if keys[K_SPACE]:
                # sound.play('space')
                self.thrust = 1.2
                if self.cooldown < 20 and self.fuel > 0:
                    self.fuel -= 1
                    self.vectorx += self.sin * self.thrust * 10
                    self.vectory += self.cos * self.thrust * 10
                    self.thrust_trail(int(body.x), int(body.y))
                    draw_trail(self.trail_list)
                if self.cooldown < 21:
                    self.cooldown += 0.2
            if keys[K_g]:
                self.enter += 1
                zzz = fonts.basic.render(" "+str(self.enter), 2, Colors.BLUE)
                s.surface.blit(zzz, (s.window_width/2, s.window_height/2))

    def rcs_thruster(self, x, y, param):
        if self.count > 0:
            if param == 'l':
                self.thrl += 0.25
                wsp1 = (x-self.camx+self.cos*8, y-self.camy-self.sin*8)
                wsp2 = (x-self.camx-self.cos*5, y-self.camy+self.sin*5)
    
            else:
                self.thrr += 0.25
                wsp1 = (x-self.camx-self.cos*8, y-self.camy+self.sin*8)
                wsp2 = (x-self.camx+self.cos*5, y-self.camy-self.sin*5)
            pygame.draw.line(s.surface, Colors.OCEAN, (x-self.camx+self.sin*6, y-self.camy+self.cos*6), wsp1, 2)
            pygame.draw.line(s.surface, Colors.OCEAN, (x-self.camx-self.sin*2, y-self.camy-self.cos*2), wsp2, 2)

    def thrust_trail(self, x, y):
        rand1 = random.randint(1, 3)
        rand2 = random.randint(1, 3)
        self.trail_list.append((int(x-self.camx-13*self.sin*rand1), int(y-self.camy-13*self.cos*rand1)))
        self.trail_list.append((int(x-self.camx-20*self.sin), int(y-self.camy-20*self.cos)))
        self.trail_list.append((int(x-self.camx-30*self.sin*rand1/rand2), int(y-self.camy-30*self.cos*rand1/rand2)))

    def counter(self):
        self.count += 1
        if self.count >= 6:
           self.count = 0

    def del_body(self, body):
        for i, o in enumerate(self.bodies):
            if o.name == body:
                del self.bodies[i]

    def load_fuel(self):
        self.fuel = self.fuel + 1
        if self.fuel > 1000:
            self.fuel = 1000

    def fuel_out(self, body1, body2, distance):
        if body1.name == 'sol' and body2.name == 'rocket':
            if distance > 10000 and self.fuel < 1:
                msg = "You ran out of self.fuel! Point of no return."
                endgame_gry = fonts.end.render(msg, 1, Colors.WHITE)
                s.surface.blit(endgame_gry, (400, 400))
                pygame.display.update()
                time.sleep(2)
                self.rockets -= 1
                self.del_body("rocket")

    def distant_bodies_remover(self, body1, body2, distance):
        if body1.name == 'sol' and body2.type != 0:
            if distance > 40000:
                self.del_body(body2.name)
                print("Body %s removed." % body2.name)

    def collisions(self, body1, body2, distance):
        # If rocket collides a star:
        if body1.type == 0 and body2.type == 1:
            if distance < body2.size:
                self.lose_rocket(body1)

        # If landing vehicle collides a star:
        if body1.type == 5 and body2.type == 1:
            if distance < body2.size:
                self.del_body(body1.name)

        # If planet collides a star or another planet:
        if body1.type == 2 and (body2.type == 1 or body2.type == 2):
            if distance < body2.size:
                self.colonies.destroy_colony(body1.name)

        # If comet, moon or planet collides a star or a planet:
        if (body1.type == 3 or body1.type == 4 or body1.type == 2) and (body2.type == 1 or body2.type == 2):
            if distance < body2.size:
                self.del_body(body1.name)

    def lose_rocket(self, body1):
        body1.velocityx = 0
        body1.velocityy = 0
        self.del_body("rocket")
        msg = "You have collided with the star!"
        gameover = fonts.end.render(msg, 1, Colors.WHITE)
        s.surface.blit(gameover, (200, 300))
        pygame.display.update()
        time.sleep(2)
        self.rockets -= 1

    def rockets_available(self):
        if self.rockets < 1:
            tresc = "You ran out of rockets. GAME OVER."
            gameover = fonts.basic.render(tresc, 1, Colors.WHITE)
            s.surface.blit(gameover, (400, 400))
            pygame.display.update()
            endgame()

    def victory_conditions(self):
        col_with_3_level = [c for c in self.colonies.c if c.level >= 3]
        if len(self.colonies.c) >= 2:
            if len(col_with_3_level) >= 2:
                print("You won!")

    def points(self):
        i = 0
        for x in range(0, 1000, 180):
            for y in range(0, 1000, 180):
                self.bodies.append(Body(str(i), 6, Colors.RED, x, y, 0, 0, 1, 1, []))
                i += 1
