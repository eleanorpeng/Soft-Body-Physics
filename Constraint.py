import math

from Vector import *
from Particle import *

class Constraint:
    node1 = None
    node2 = None
    target = 0.0
    stiff = 1.0
    damp = 0.0

    def __init__(self, p1, p2, s, d=None):
        self.node1 = p1
        self.node2 = p2
        self.stiff = s
        if d is None:
            self.target = math.sqrt((p2.position.x - p1.position.x)**2 + (p2.position.y - p1.position.y) ** 2)
        else:
            self.target = d

    def relax(self):
        d = self.node2.position - self.node1.position
        f = 0.5 * self.stiff * (d.length() - self.target) * d.normalize()
        if self.node1.material.mass != 0.0 and not self.node2.material.mass:
            self.node1.apply_impulse(2.0 * f)
        elif not self.node1.material.mass and self.node2.material.mass != 0.0:
            self.node2.apply_impulse(2.0 * -f)
        else:
            self.node1.apply_impulse(f)
            self.node2.apply_impulse(-f)
