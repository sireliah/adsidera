# -*- coding: utf-8 -*-

import time
import math
import random
import pygame
from pygame import gfxdraw
from pygame.locals import KEYDOWN, K_RETURN, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT, K_c, K_g, QUIT
from numpy import mean

from bodies import Body, BodiesCreator
from camera import camera
from colonies import Colonies
from conf import fonts, s, sprites, sound, Colors, GameSettings, endgame
from drawing import Drawing, HUD, draw_trail
from mainmenu import Menu
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
        self.velocity_components_x, self.velocity_components_y = [], []
        self.cooldown = 0
        self.fuel = 1000
        self.fuel_dist = 0
        self.vectorx, self.vectory = 1, 1
        self.landerx, self.landery = 0, 0
        self.rocket_center_x, self.rocket_center_y = 15, 43
        self.rocket_thruster_left, self.rocket_thruster_right = 0, 0
        self.rocket_image = sprites.rocket_image.copy()
        self.colonies = Colonies(self.rocket_resources)
        self.drawing = Drawing(self.camx, self.camy, self.count, sprites, BodiesCreator.generate_stars())

    def play(self):

        sound.play('music')

        while True:
            self.counter()
            self.victory_conditions()
            self.landing_vehicle_lock = False

            # Fill the background with black to cleanup the screen from old frames.
            s.surface.fill(Colors.BLACK)

            self.sin = math.sin(self.rocket_angle)
            self.cos = math.cos(self.rocket_angle)

            # Render static gauges, map, etc.
            self.hud = HUD(self.bodies, sprites, self.sin, self.cos, self.clock, self.rockets, self.landing_vehicles)

            # Pygame event loop.
            self.events()

            # Emulate physics.
            self.bodies_interactions()

            new_center_x, new_center_y = self.transform_rocket_image()
            self.rocket_center_x += new_center_x
            self.rocket_center_y += new_center_y

            self.check_rockets_available()

            """
            Calculate the force applied to the rocket based on mean velocity components from last iteration.
            This will be used in the gravimeter.
            """
            self.gforce = (mean(self.velocity_components_x), mean(self.velocity_components_y))

            self.addd.comets()
            self.drawing.draw_stars(self.camx, self.camy)

            # Empty old velocity components lists.
            del self.velocity_components_x[:]
            del self.velocity_components_y[:]

            # Tick the game clock and draw all images.
            self.clock.tick_busy_loop(GameSettings.FPS)
            pygame.display.flip()

    def bodies_physics(self, body):
        if [i for i in self.bodies if i.name == 'rocket']:

            if body.name == 'rocket':
                body.x += body.velocityx + self.vectorx / GameSettings.RETARDATION
                body.y += body.velocityy + self.vectory / GameSettings.RETARDATION
                self.camx, self.camy = camera(self.camx, self.camy, body, center_on='rocket')

            elif body.type == 'landing_vehicle':
                lander_angle = math.atan2(self.landerx, self.landery)
                if self.lander_dist < 200:
                    sx = body.velocityx - (math.sin(lander_angle) / 2)
                    sy = body.velocityy - (math.cos(lander_angle) / 2)
                else:
                    sx = body.velocityx / GameSettings.RETARDATION
                    sy = body.velocityy / GameSettings.RETARDATION
                body.x += sx
                body.y += sy
            elif body.type == '???':
                pass
            else:
                body.x += body.velocityx / GameSettings.RETARDATION
                body.y += body.velocityy / GameSettings.RETARDATION

        else:
            body.x += body.velocityx / GameSettings.RETARDATION
            body.y += body.velocityy / GameSettings.RETARDATION
            self.camx, self.camy = camera(self.camx, self.camy, body, center_on='terra')

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
            self.drawing.draw_objects(
                body1,
                self.camx,
                self.camy,
                self.sin,
                self.cos,
                self.rocket_center_x,
                self.rocket_center_y,
                self.count,
                self.colonies
            )

            for body2 in self.bodies:
                if body1 != body2:

                    # Distance between two bodies.
                    distance = math.sqrt(
                        (body1.x - body2.x) ** 2 + (body1.y - body2.y) ** 2
                    )

                    self.collisions(body1, body2, distance)
                    self.fuel_out(body1, body2, distance)

                    if distance < 15:
                        distance = 14
                    if distance < 150000:

                        """
                        Newton's law of universal gravitation.*
                        *works only for non-superlarge distances because of the performance reasons. ᕙ(⇀‸↼‶)ᕗ
                        """

                        # Calculate the gravitational force between two bodies.
                        F = GameSettings.G_CONSTANT * (body1.mass * body2.mass / (distance * distance))

                        # Calculate the acceleration of the body.
                        a = F / body1.mass

                        # Calculate velocity components.
                        componentx = (a * (body1.x - body2.x)) / distance
                        componenty = (a * (body1.y - body2.y)) / distance

                        if body1.name == 'rocket':
                            self.velocity_components_x.append(componentx)
                            self.velocity_components_y.append(componenty)

                            if body2.type == 'planet':
                                self.fuel_dist = distance
                                if self.fuel_dist < 30:
                                    self.load_fuel(body2)
                                    pygame.draw.circle(
                                        s.surface, Colors.GREEN,
                                        (int(body1.x - self.camx), int(body1.y - self.camy)),
                                        30, 2
                                    )

                        if 'landing vehicle' in body1.name:
                            if body2.type == 'planet':
                                self.lander_dist = distance
                                if distance < 200:
                                    self.landerx = componentx
                                    self.landery = componenty
                                    if distance < 17:
                                        self.colonies.colony_deployment(body1, body2, distance, self.rocket_resources)
                                        self.del_body(body1.name)
                            elif body2.type == 'rocket':
                                # Distance from rocket to landing vehicle
                                self.rdist = distance

                        """
                        If rocket was just destroyed, we store the velocity component between Sun and Earth
                        to later calculate in which direction should we launch the new rocket.
                        """
                        if (not [i for i in self.bodies if i.name == 'rocket'] and
                                body1.name == 'terra' and body2.name == 'sol'):
                            self.terra_sol_component_x = componentx
                            self.terra_sol_component_y = componenty

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

    def transform_rocket_image(self):
        """
        Get the rocket rectangle and rotate it.
        Return new center, because rectangle is deformed in the process.
        """
        oldrect = sprites.rocket_image.get_rect()
        sprites.rocket_image = pygame.transform.rotozoom(self.rocket_image, int(math.degrees(self.rocket_angle)), 1)
        newrect = sprites.rocket_image.get_rect()
        new_center_x = newrect.centerx - oldrect.centerx
        new_center_y = newrect.centery - oldrect.centery
        return new_center_x, new_center_y

    def events(self):
        """
        Pygame event loop.
        """

        for event in pygame.event.get():
            for body in self.bodies:
                if body.name == 'terra':

                    # This position will be later used for the starting point of the rocket.
                    self.terra_x = body.x
                    self.terra_y = body.y

                if event.type == QUIT:
                    endgame()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        endgame()

                    elif event.key == K_c and body.name == 'rocket':
                        self.thrust = self.thrust - 0.1
                    elif event.key == K_RETURN and body.name == 'terra':
                        if not [i for i in self.bodies if i.name == 'rocket']:

                            # Direction in which rocket will launch from Earth.
                            # Just not to catapult rocket in the Sun. :D
                            direction = math.atan2(self.terra_sol_component_y, self.terra_sol_component_x)
                            vx = math.cos(direction)
                            vy = math.sin(direction)
                            self.bodies.insert(
                                0,
                                Body(
                                    'rocket',
                                    type='rocket',
                                    color=Colors.WHITE,
                                    x=self.terra_x + 1, y=self.terra_y + 1,
                                    velocityx=vx * 6, velocityy=vy * 6,
                                    mass=1,
                                    size=1,
                                )
                            )
                            self.fuel = 1000
                            self.landing_vehicles = 3
                            sound.play('takeoff')
                            self.vectorx = 0
                            self.vectory = 0

                    elif event.key == K_RETURN and body.name == 'rocket':
                        self.launch_landing_vehicle(body)

    def launch_landing_vehicle(self, body):
        landing_vehicles = [i for i in self.bodies if type == "landing_vehicle"]
        if landing_vehicles:
            if self.rdist < 30:
                self.rocket_circle += 10
                self.rdist = 100
                self.del_body(landing_vehicles[0].name)
                self.landing_vehicles += 1
                self.landing_vehicle_lock = True

        if self.landing_vehicles > 0 and not self.landing_vehicle_lock:
            self.bodies.insert(
                0,
                Body(
                    'landing vehicle %s' % random.randint(1, 100),
                    type='landing_vehicle',
                    color=Colors.GINGER,
                    x=body.x, y=body.y,
                    velocityx=body.velocityx + self.sin * 30,
                    velocityy=body.velocityy + self.cos * 30,
                    mass=1,
                    size=2,
                )
            )
            self.rocket_circle -= 10
            self.landing_vehicles -= 1
            sound.play('takeoff')
            self.landing_vehicle_lock = True

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

                    # Generate and draw rocket exhaust.
                    self.thrust_trail(int(body.x), int(body.y))
                    draw_trail(self.trail_list)
                if self.cooldown < 21:
                    self.cooldown += 0.2
            if keys[K_g]:
                self.enter += 1
                zzz = fonts.basic.render(" "+str(self.enter), 2, Colors.BLUE)
                s.surface.blit(zzz, (s.window_width/2, s.window_height/2))

    def rcs_thruster(self, x, y, param):
        """
        Engine that rotates the rocket.
        """
        if self.count > 0:
            if param == 'l':
                self.rocket_thruster_left += 0.25
                coord1 = (x-self.camx+self.cos*8, y-self.camy-self.sin*8)
                coord2 = (x-self.camx-self.cos*5, y-self.camy+self.sin*5)

            else:
                self.rocket_thruster_right += 0.25
                coord1 = (x-self.camx-self.cos*8, y-self.camy+self.sin*8)
                coord2 = (x-self.camx+self.cos*5, y-self.camy-self.sin*5)

            pygame.draw.line(
                s.surface, Colors.OCEAN,
                (x - self.camx + self.sin * 6, y-self.camy+self.cos*6),
                coord1, 2
            )
            pygame.draw.line(
                s.surface,
                Colors.OCEAN,
                (x - self.camx - self.sin * 2, y - self.camy - self.cos * 2),
                coord2, 2
            )

    def thrust_trail(self, x, y):
        """
        Generate rocket exhaust.
        """
        rand1 = random.randint(1, 3)
        rand2 = random.randint(1, 3)
        self.trail_list.append(
            (int(x - self.camx - 13 * self.sin * rand1), int(y - self.camy - 13 * self.cos * rand1))
        )
        self.trail_list.append(
            (int(x - self.camx - 20 * self.sin), int(y - self.camy - 20 * self.cos))
        )
        self.trail_list.append(
            (int(x - self.camx - 30 * self.sin * rand1 / rand2), int(y - self.camy - 30 * self.cos * rand1 / rand2))
        )

    def counter(self):
        self.count += 1
        if self.count >= 6:
            self.count = 0

    def del_body(self, body):
        """
        Remove the body from the list.
        """
        for i, o in enumerate(self.bodies):
            if o.name == body:
                del self.bodies[i]

    def load_fuel(self, body):
        """
        Add the fuel to the rocket tank.
        """
        loaded_fuel_amount = 1

        # Loading fuel from colonies should be faster.
        if body.name in [colony.planet for colony in self.colonies]:
            loaded_fuel_amount = 100

        self.fuel = self.fuel + loaded_fuel_amount
        if self.fuel > 1000:
            self.fuel = 1000

    def fuel_out(self, body1, body2, distance):
        """
        If rocket is very far away and have very little fuel, it obviously won't be able go back.
        """
        if body1.name == 'sol' and body2.name == 'rocket':
            if distance > 10000 and self.fuel < 1:
                msg = "You ran out of self.fuel! Point of no return."
                endgame = fonts.end.render(msg, 1, Colors.WHITE)
                s.surface.blit(endgame, (400, 400))
                pygame.display.update()
                time.sleep(2)
                self.rockets -= 1
                self.del_body("rocket")

    def distant_bodies_remover(self, body1, body2, distance):
        """
        Body garbage collector to relieve the cpu.
        """
        if body1.name == 'sol' and body2.type != 'rocket':
            if distance > 40000:
                self.del_body(body2.name)
                print("Body %s removed." % body2.name)

    def collisions(self, body1, body2, distance):
        # If rocket collides a star:
        if body1.type == 'rocket' and body2.type == 'star':
            if distance < body2.size:
                self.rocket_destroyed(body1)

        # If landing vehicle collides a star:
        if body1.type == 'landing_vehicle' and body2.type == 'star':
            if distance < body2.size:
                self.del_body(body1.name)

        # If planet collides a star or another planet:
        if body1.type == 'planet' and (body2.type == 'star' or body2.type == 'planet'):
            if distance < body2.size:
                self.colonies.destroy_colony(body1.name)

        # If comet, moon or planet collides a star or a planet:
        if body1.type in ('comet', 'planet', 'moon') and (body2.type in ('star', 'planet')):
            if distance < body2.size:
                self.del_body(body1.name)

    def rocket_destroyed(self, body1):
        """
        When the rocket collided the star.
        """
        body1.velocityx = 0
        body1.velocityy = 0
        self.del_body("rocket")
        msg = "You have collided with the star!"
        gameover = fonts.end.render(msg, 1, Colors.WHITE)
        s.surface.blit(gameover, (200, 300))
        pygame.display.update()
        time.sleep(2)
        self.rockets -= 1

    def check_rockets_available(self):
        if self.rockets < 1:
            tresc = "You ran out of rockets. GAME OVER."
            gameover = fonts.basic.render(tresc, 1, Colors.WHITE)
            s.surface.blit(gameover, (400, 400))
            pygame.display.update()
            endgame()

    def victory_conditions(self):
        col_with_3_level = [c for c in self.colonies if c.level >= 3]
        if len(self.colonies) >= 2 and len(col_with_3_level) >= 2:
            msg = "You won!"
            gameover = fonts.end.render(msg, 1, Colors.WHITE)
            s.surface.blit(gameover, (200, 300))
            pygame.display.update()
            sound.play('win')
            time.sleep(27)
            endgame()
