
import math
import random

from conf import Colors


class Body(object):

    def __init__(self, name='', type='', color='', x=0, y=0, velocityx=0, velocityy=0, mass=0, size=0, trail=[]):
        self.name = name
        self.type = type
        self.color = color
        self.x = x
        self.y = y
        self.velocityx = velocityx
        self.velocityy = velocityy
        self.mass = mass
        self.size = size
        self.trail = []
        """
        types:
        0 - maneuverable object (rocket)
        1 - star
        2 - planet
        3 - moon
        4 - other
        5 - landing vehicle
        """


class BodiesCreator(object):

    def __init__(self, star_names, planet_names):
        self.bodies = []
        self.star_names = star_names
        self.planet_names = planet_names
        self.solar_system_bodies()
        self.colors = (Colors.WHITE, Colors.YELLOW, Colors.RED, Colors.ORANGE, Colors.BLUE, Colors.OCEAN, Colors.GINGER, Colors.IOVIS)
        # self.bodies.append(Body('Alpha Centauri', 1, Colors.RED, 400, 350, 2, 0, 50000, 22, (0,0)))

    def solar_system_bodies(self):
        self.bodies.append(Body('sol', 1, Colors.WHITE, 400, 350, 2, 0, 12000, 22, (0, 0)))
        self.bodies.append(Body('rocket', 0, Colors.WHITE, 300, -150, 0, 0, 1, 1, (0, 0)))
        self.bodies.append(Body('mars', 2, Colors.ORANGE, 400, 10, 27, 0, 350, 7, (0, 0)))
        self.bodies.append(Body('terra', 2, Colors.OCEAN, 400, 140, 30, 0, 400, 9, (0, 0)))
        self.bodies.append(Body('iovis', 2, Colors.IOVIS, 400, -300, 22, 0, 1000, 12, (0, 0)))
        self.bodies.append(Body('saturnus', 2, Colors.YELLOW, 400, -700, 20, 0, 600, 10, (0, 0)))
        self.bodies.append(Body('luna', 3, Colors.WHITE, 400, 150, 3, 0, 8, 4, (0, 0)))

    def random_int(self):
        self.randint = random.randint(-8000, 8000)
        while (self.randint > -2000) or (self.randint < 2000):
            self.randint = random.randint(-8000, 8000)
            if self.randint < -2000 or self.randint > 2000:
                return self.randint
                break

    def rand_systems(self):
        self.stars_num = random.randint(1, 5)

        def rand_planet(dist, mass_coe):
            self.exoplanet_color = random.sample(self.colors, 1)
            self.planet_name = ''.join(random.sample(self.planet_names, 1))
            planet_mass = int(self.mass*mass_coe)
            planet_radius = int(random.randint(int(self.radius*0.1), int(self.radius*0.7)))
            self.bodies.append(
                Body(
                    self.planet_name, 2, self.exoplanet_color[0], self.x+dist, self.y+dist,
                    35, 0, planet_mass, planet_radius, (0, 0)
                )
            )

        for a in range(self.stars_num):
            self.star_name = ''.join(random.sample(self.star_names, 1))
            self.color = random.sample(self.colors, 1)
            self.mass = random.randint(900, 120000)
            self.radius = random.randint(10, 50)
            for star in self.bodies:
                if star.type == 1:
                    self.x = self.random_int()
                    self.y = self.random_int()
                    dist = math.sqrt((star.x-self.x)**2 + (star.y-self.y)**2)
                    if dist > 2000:
                        self.bodies.append(
                            Body(self.star_name, 1, self.color[0], self.x, self.y, 0, 0, self.mass, self.radius, (0, 0))
                        )
                        self.exoplanet = random.randint(1, 6)
                        self.planet_name = ''.join(random.sample(self.planet_names, 1))

                        if self.exoplanet >= 2:
                            rand_planet(300, 0.012)    
                        if self.exoplanet >= 4:
                            rand_planet(600, 0.008)
                        if self.exoplanet == 6:
                            rand_planet(800, 0.010)
                        break
        return self.bodies

    def comets(self):
        randint = random.randint(0, 10000)
        if randint > 9990:
            print("Comet!")
            mass = random.randint(10, 50)
            size = random.randint(3, 10)
            x = self.random_int()
            y = self.random_int()
            velocityx = random.randint(-1000, 1000)
            velocityy = random.randint(-1000, 1000)
            self.bodies.append(
                Body('cometa', 4, Colors.GRAY, x, y, velocityx, velocityy, mass, size, (0, 0))
            )

    @staticmethod
    def generate_stars():
        """
        Generate stars for the background.
        """
        stars = []
        for a in range(5000):
            wsp1 = random.randint(-8000, 8000)
            wsp2 = random.randint(-8000, 8000)
            stars.append((wsp1, wsp2))
        return stars

    def remove_bodies(self):
        del self.bodies[:]
