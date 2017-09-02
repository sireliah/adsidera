
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
        self.trail = [(0, 0)]
        """
        types:
        0 - maneuverable object (rocket)
        1 - star
        2 - planet
        3 - moon
        4 - other
        5 - landing vehicle
        6 - ???
        """


class BodiesCreator(object):

    def __init__(self, star_names, planet_names):
        self.bodies = []
        self.star_names = star_names
        self.planet_names = planet_names
        self.solar_system_bodies()
        self.colors = (
            Colors.WHITE, Colors.YELLOW, Colors.RED, Colors.ORANGE,
            Colors.BLUE, Colors.OCEAN, Colors.GINGER, Colors.IOVIS
        )

    def solar_system_bodies(self):
        """
        Add Solar System bodies. Not all of them, because it's nearly impossible to make sure
        they stay in stable orbits for long enough.
        """
        self.bodies.append(
            Body(
                'sol',
                type='star',
                color=Colors.WHITE,
                x=400, y=350,
                velocityx=2, velocityy=0,
                mass=12000,
                size=22,
            )
        )
        self.bodies.append(
            Body(
                'rocket',
                type='rocket',
                color=Colors.WHITE,
                x=300, y=-150,
                velocityx=0, velocityy=0,
                mass=1,
                size=1,
            )
        )
        self.bodies.append(
            Body(
                'mars',
                type='planet',
                color=Colors.ORANGE,
                x=400, y=10,
                velocityx=27, velocityy=0,
                mass=350,
                size=7,
            )
        )
        self.bodies.append(
            Body(
                'terra',
                type='planet',
                color=Colors.OCEAN,
                x=400, y=140,
                velocityx=30, velocityy=0,
                mass=400,
                size=9,
            )
        )
        self.bodies.append(
            Body(
                'iovis',
                type='planet',
                color=Colors.IOVIS,
                x=400, y=-300,
                velocityx=22, velocityy=0,
                mass=1000,
                size=12,
            )
        )
        self.bodies.append(
            Body(
                'saturnus',
                type='planet',
                color=Colors.YELLOW,
                x=400, y=-700,
                velocityx=20, velocityy=0,
                mass=600,
                size=10,
            )
        )
        self.bodies.append(
            Body(
                'luna',
                type='moon',
                color=Colors.WHITE,
                x=400, y=150,
                velocityx=3, velocityy=0,
                mass=8,
                size=4,
            )
        )

    def random_int(self):
        self.randint = random.randint(-8000, 8000)
        while (self.randint > -2000) or (self.randint < 2000):
            self.randint = random.randint(-8000, 8000)
            if self.randint < -2000 or self.randint > 2000:
                return self.randint
                break

    def rand_systems(self):
        """
        Generate random stars with planets.
        """
        self.stars_num = random.randint(1, 5)

        def rand_planet(dist, mass_coe):
            self.exoplanet_color = random.sample(self.colors, 1)
            self.planet_name = ''.join(random.sample(self.planet_names, 1))
            planet_mass = int(self.mass * mass_coe)
            planet_radius = int(random.randint(int(self.radius*0.1), int(self.radius*0.7)))
            self.bodies.append(
                Body(
                    self.planet_name,
                    type='planet',
                    color=self.exoplanet_color[0],
                    x=self.x + dist, y=self.y + dist,
                    velocityx=35, velocityy=0,
                    mass=planet_mass,
                    size=planet_radius,
                )
            )

        for a in range(self.stars_num):
            self.star_name = ''.join(random.sample(self.star_names, 1))
            self.color = random.sample(self.colors, 1)
            self.mass = random.randint(900, 120000)
            self.radius = random.randint(10, 50)
            for star in self.bodies:
                if star.type == 'star':
                    self.x = self.random_int()
                    self.y = self.random_int()
                    dist = math.sqrt((star.x-self.x)**2 + (star.y-self.y)**2)
                    if dist > 2000:
                        self.bodies.append(
                            Body(
                                self.star_name,
                                type='star',
                                color=self.color[0],
                                x=self.x, y=self.y,
                                velocityx=0, velocityy=0,
                                mass=self.mass,
                                size=self.radius,
                            )
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
                Body(
                    'cometa',
                    type='cometa',
                    color=Colors.GRAY,
                    x=x, y=y,
                    velocityx=velocityx, velocityy=velocityy,
                    mass=mass,
                    size=size,
                )
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
