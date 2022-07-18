from Vector import *
from Particle import *
from Constraint import *
from Composite import *
from Material import *

class World:
    size = Vector(0.0, 0.0)
    hsize = Vector(0.0, 0.0)
    gravity = Vector(0.0, 0.0)
    step = 0
    delta = 0.0

    particles = list()
    constraints = list()
    composites = list()

    def __init__(self, s=Vector(0.0, 0.0), g=Vector(0.0, 9.8), t=8):
        self.size = s
        self.hsize = 0.5 * s
        self.gravity = g
        if t < 1:
            self.step = 1
            self.delta = 1.0
        else:
            self.step = t
            self.delta = 1.0 / self.step

    def simulate(self):
        for i in range(self.step):
            for particle in self.particles:
                particle.accelerate(self.gravity)
                particle.simulate()
                particle.restrain()
                particle.reset_forces()
            for constraint in self.constraints:
                constraint.relax()

    def add_particle(self, x, y, mat=None):
        particle = Particle(self, x, y, mat)
        self.particles.append(particle)
        return particle

    def add_constraint(self, p1, p2, s, d=None):
        constraint = Constraint(p1, p2, s, d)
        self.constraints.append(constraint)
        return constraint

    def add_composite(self, *params):
        composite = Composite(params)
        self.composites.append(composite)
        return composite