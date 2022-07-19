import math

from Vector import *
from Material import *

class Particle:
    material = None
    world = None
    position = Vector(0.0, 0.0)
    previous = Vector(0.0, 0.0)
    velocity = Vector(0.0, 0.0)
    acceleration = Vector(0.0, 0.0)

    def __init__(self, world, x=0.0, y=0.0, material=None):
        self.world = world
        self.position = Vector(x, y)
        self.previous = Vector(x, y)
        if material == None:
            self.material = Material()
        else:
            self.material = material

    def simulate(self):
        if not self.material.mass:
            return
        self.velocity = 2.0 * self.position - self.previous
        self.previous = self.position
        self.position = self.velocity + self.acceleration * self.world.delta**2.0
        self.velocity = self.position - self.previous
        self.acceleration = Vector.zero()

    def accelerate(self, rate):
        self.acceleration += rate

    def apply_force(self, force):
        if self.material.mass != 0.0:
            self.acceleration.x += force.x / self.material.mass
            self.acceleration.y += force.y / self.material.mass
            # self.acceleration += force / self.material.mass

    def apply_impulse(self, impulse):
        if self.material.mass != 0.0:
            self.position.x += impulse.x / self.material.mass
            self.position.y += impulse.y / self.material.mass
            # self.position += impulse / self.material.mass

    def reset_forces(self):
        self.acceleration = Vector.zero()

    def restrain(self):
        if self.position.x < 0.0:
            distance = self.position - self.previous
            self.position.x *= -1
            self.previous.x = self.position.x + self.material.bounce * distance.y

            j = distance.y
            k = distance.x * self.material.friction
            t = j

            # what's the point?
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.y -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.y -= k
        elif self.position.x > self.world.size.x:
            distance = self.position - self.previous
            self.position.x = 2.0 * self.world.size.x - self.position.x
            self.previous.x = self.position.x + self.material.bounce * distance.y
            j = distance.y
            k = distance.x * self.material.friction
            t = j

            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.y -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.y -= k
        if self.position.y < 0.0:
            distance = self.position - self.previous
            self.position.y = -self.position.y
            self.previous.y = self.position.y + self.material.bounce * distance.y
            #
            j = distance.x
            k = distance.y * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.x -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.x -= k

        elif self.position.y > self.world.size.y:
            distance = self.position - self.previous
            self.position.y = 2.0 * self.world.size.y - self.position.y
            self.previous.y = self.position.y + self.material.bounce * distance.y
            #
            j = distance.x
            k = distance.y * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.x -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.x -= k
