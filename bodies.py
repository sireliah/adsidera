
import math
import random

from conf import Colors


class Body(object):

    def __init__(self, name='', type='', color='', x=0, y=0, velocity_x=0, velocity_y=0, mass=0, size=0, trail=[]):
        self.name = name
        self.type = type
        self.color = color
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.mass = mass
        self.size = size
        self.trail = [(0, 0)]
        """
        types:
        - maneuverable object (rocket)
        - star
        - planet
        - moon
        - other
        - landing vehicle
        """


class BodyCreator(object):

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
                velocity_x=2, velocity_y=0,
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
                velocity_x=0, velocity_y=0,
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
                velocity_x=27, velocity_y=0,
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
                velocity_x=30, velocity_y=0,
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
                velocity_x=22, velocity_y=0,
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
                velocity_x=20, velocity_y=0,
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
                velocity_x=3, velocity_y=0,
                mass=8,
                size=4,
            )
        )

    def generate_random_int_range(self):
        """
        Keep picking coordinates untill they match certain criteria.randint

        yes yes yes yes yes
        yes |---------| yes
        yes | no no no| yes
        yes | no no no| yes
        yes |---------| yes
        yes yes yes yes yes

        """
        randint = random.randint(-8000, 8000)
        while (randint > -2000) or (randint < 2000):
            randint = random.randint(-8000, 8000)
            if randint < -2000 or randint > 2000:
                return randint

    def rand_systems(self):
        """
        Generate random stars with planets.
        """
        self.stars_num = random.randint(1, 5)

        def rand_planet(dist, mass_coe):
            """
            Generate planet that should be in proportional size and mass to it's start.
            """
            self.exoplanet_color = random.sample(self.colors, 1)
            self.planet_name = ''.join(random.sample(self.planet_names, 1))
            planet_mass = int(self.mass * mass_coe)
            planet_radius = int(random.randint(int(self.radius * 0.1), int(self.radius * 0.7)))
            self.bodies.append(
                Body(
                    self.planet_name,
                    type='planet',
                    color=self.exoplanet_color[0],
                    x=self.x + dist, y=self.y + dist,
                    velocity_x=35, velocity_y=0,
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
                    self.x = self.generate_random_int_range()
                    self.y = self.generate_random_int_range()
                    dist = math.sqrt((star.x - self.x) ** 2 + (star.y - self.y) ** 2)

                    if dist > 2000:
                        self.bodies.append(
                            Body(
                                self.star_name,
                                type='star',
                                color=self.color[0],
                                x=self.x, y=self.y,
                                velocity_x=0, velocity_y=0,
                                mass=self.mass,
                                size=self.radius,
                            )
                        )
                        self.exoplanet_variation = random.randint(1, 6)
                        self.planet_name = ''.join(random.sample(self.planet_names, 1))

                        if self.exoplanet_variation >= 2:
                            rand_planet(300, 0.012)
                        if self.exoplanet_variation >= 4:
                            rand_planet(600, 0.008)
                        if self.exoplanet_variation == 6:
                            rand_planet(800, 0.010)
                        break

        return self.bodies

    def comets(self):
        randint = random.randint(0, 10000)
        if randint > 9990:
            mass = random.randint(10, 50)
            size = random.randint(3, 10)
            x = self.generate_random_int_range()
            y = self.generate_random_int_range()
            velocity_x = random.randint(-1000, 1000)
            velocity_y = random.randint(-1000, 1000)
            self.bodies.append(
                Body(
                    'cometa',
                    type='cometa',
                    color=Colors.GRAY,
                    x=x, y=y,
                    velocity_x=velocity_x, velocity_y=velocity_y,
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
