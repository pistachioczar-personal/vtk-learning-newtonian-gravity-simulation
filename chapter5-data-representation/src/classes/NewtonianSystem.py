
from typing import Final
from support import vector_math as vm
from classes import NewtonianBody


class NewtonianSystem:

    GRAVITATIONAL_CONSTANT: Final = 0.000295913120346

    def __init__(self, bounds: list):
        self._bodies = []
        self._bounds = bounds
        

    def add_body(self, body):
        self._bodies.append(body)

    def add_bodies(self, bodies: list):
        self._bodies.extend(bodies)

    def get_bodies(self):
        return self._bodies

    def get_bounds(self):
        return self._bounds

    def get_system_kinetic(self):
        total_kinetic_energy = 0
        for body in self._bodies:
            if isinstance(body, NewtonianBody):
                total_kinetic_energy += body.get_my_kinetic()
        return total_kinetic_energy

    def get_system_potential(self):
        total_potential_energy = 0
        for i in range(len(self._bodies)):
            for j in range(i + 1, len(self._bodies)):
                if isinstance(self._bodies[i], NewtonianBody) and isinstance(self._bodies[j], NewtonianBody):
                    distance = (vm.add_vecs(self._bodies[i].get_position(), vm.scale_vec(-1, self._bodies[j].get_position()))).Norm()
                    total_potential_energy -= (self.GRAVITATIONAL_CONSTANT * self._bodies[i].get_mass() * self._bodies[j].get_mass()) / distance
        return total_potential_energy

    def get_system_total_energy(self):
        return self.get_system_kinetic() + self.get_system_potential()