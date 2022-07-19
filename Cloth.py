import random
import pygame as game

from App import *
from VerletPhysics import *

class Cloth(App):
    world = World(Vector(640.0, 480.0), Vector(0, 2), 2)
    mousepos = Vector()
    previous = Vector()
    strength = 3.0
    radius = 30

    def initialize(self):
        cloth = self.world.add_composite()

        nodes = list()
        const = list()
        minX = 140
        maxX = 500
        minY = 50
        maxY = 400
        step = 12
        size = Vector((maxX-minX) / step, (maxY-minY) / step)

        for y in range(step):
            nodes.append(list())
            for x in range(step):
                nodes[y].append(self.world.add_particle(minX + x * size.x, minY + y * size.y))
                if not y:
                    nodes[y][x].material.mass = 0.0
                elif y == step - 1:
                    nodes[y][x].apply_force(Vector(50.0, random.random() * -500.0))

        for y in range(step):
            for x in range(1, step):
                const.append(self.world.add_constraint(nodes[y][x-1], nodes[y][x], 1.0))

        for y in range(1, step):
            for x in range(step):
                const.append(self.world.add_constraint(nodes[y-1][x], nodes[y][x], 1.0))

        cloth.add_particles(nodes)
        cloth.add_constraints(const)

    def update(self):
        self.mousepos = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        if game.mouse.get_pressed()[0]:
            force = (self.mousepos - self.previous) * self.strength
            for particle in self.world.particles:
                if self.mousepos.distance(particle.position) < self.radius:
                    particle.apply_force(force)
        self.previous = self.mousepos

        if game.key.get_pressed()[game.K_ESCAPE]:
            self.exit()
        self.world.simulate()

    def render(self):
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (255, 255, 255), pos1, pos2, 2)
        game.display.update()

if __name__ == "__main__":
    app = Cloth("Simulated Cloth", 640, 480, 30)
    app.run()