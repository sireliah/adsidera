import pygame

from conf import s, fonts, Colors


class Colony(object):

    def __init__(self, planet, resources, level):
        self.planet = planet
        self.resources = resources
        self.level = level


class Colonies(list):

    """
    Colonies implemented as list of Colony objects.
    A colony has level based on the number of landing vehicles that landed on the planet.
    """

    def __init__(self, rocket_resources):
        self.rocket_resources = rocket_resources

    def colony_deployment(self, body1, body2, distance, rocket_resources):
        self.rocket_resources = rocket_resources

        if body1.type == 'landing_vehicle' and (body2.type in ('planet', 'other')) and body2.name != 'terra':
            if distance < 20:

                # If there is no colony on this planet, add one.
                if not [i for i in self if i.planet == body2.name]:
                    self.append(Colony(body2.name, 0, 0))

                # If there is a colony already, raise it's level.
                else:
                    for a in self:
                        if a.planet == body2.name:
                            a.resources += 10

    def destroy_colony(self, planet):
        for i, c in enumerate(self):
            if c.planet == planet:
                print("Colony %s destroyed!" % c.planet)
                del self[i]

    def resources_terra(self, body1, body2, distance):
        if (body1.type == 'rocket' and body2.name == 'terra' and distance < 16):
            return True
        return False

    def show_col(self, kamerax, kameray):
        for i, colony in enumerate(self):
            if colony.resources >= 20:
                colony.level = 3
            elif colony.resources >= 10:
                colony.level = 2
            elif colony.resources >= 0:
                colony.level = 1

            if colony.level > 0:
                tekst_colony = fonts.basic.render(
                    "%s colony, level: %s" % (colony.planet, colony.level), 2, Colors.GINGER
                )
                s.surface.blit(tekst_colony, (s.window_width - 300, s.window_height / 20 * i))

    def colony_caption(self, body, camx, camy):
        for col in self:
            if col.planet == body.name:
                pygame.draw.line(
                    s.surface, Colors.ORANGE,
                    (int(body.x - camx + 15), int(body.y - camy + 12)),
                    (int(body.x - camx + 15 + col.resources), int(body.y - camy + 12)),
                    4
                )
                koll = fonts.desc.render("Colony level %s " % col.level, 1, Colors.GINGER)
                s.surface.blit(koll, (int(body.x-camx+23), int(body.y-camy+41)))
