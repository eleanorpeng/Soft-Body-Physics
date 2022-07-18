import pygame as game
from App import *
from VerletPhysics import *

class Square(App):
    world = World(Vector(640.0, 480.0), Vector(0, 2), 4)

    grabbed = None
    radius = 20
    strength = 0.2

    def initialize(self):
        mat = Material(1.0, 1.0, 1.0)
        self.world.add_particle(270, 100, mat)
        self.world.add_particle(470, 100, mat)
        self.world.add_particle(470, 300, mat)
        self.world.add_particle(270, 300, mat)

        self.world.add_constraint(self.world.particles[0], self.world.particles[1], 0.2)
        self.world.add_constraint(self.world.particles[1], self.world.particles[2], 0.2)
        self.world.add_constraint(self.world.particles[2], self.world.particles[3], 0.2)
        self.world.add_constraint(self.world.particles[3], self.world.particles[0], 0.2)
        self.world.add_constraint(self.world.particles[0], self.world.particles[2], 0.2)
        self.world.add_constraint(self.world.particles[1], self.world.particles[3], 0.2)

        self.world.particles[0].apply_impulse(Vector(0.0, -7.0))

    def update(self):
        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.closest_point()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
                force = (mouse - self.grabbed.position) * self.strength
                self.grabbed.apply_impulse(force)
        else:
            self.grabbed = None

        if game.key.get_pressed()[game.K_ESCAPE]:
            self.exit()
        self.world.simulate()

    def render(self):
        self.screen.fill((24, 24, 24))
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 0, 0), pos, 10, 0)
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (255, 0, 0), pos1, pos2, 2)
        game.display.update()

    def closest_point(self):
        mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        closest = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest = particle
                distance = d
        return closest, distance

if __name__ == '__main__':
    app = Square("Square", 640, 480, 30)
    app.run()