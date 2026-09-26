from .Body import Body
from typing import Final
from vtkmodules.vtkCommonDataModel import vtkVector3d

#importing from support
import sys
sys.path.append('../support')
from support import vector_math as vm


class NewtonianBody(Body):

    GRAVITATIONAL_CONSTANT: Final = 0.000295913120346

    def __init__(self, position: vtkVector3d, radius, velocity: vtkVector3d, gravity: vtkVector3d, mass):
        super().__init__(position, radius)
        self.__mass = mass
        self.__velocity = velocity
        self.__gravity = gravity


    #Getters and Setters
    def set_mass(self, mass):
        if not isinstance(mass, (int, float)):
            raise TypeError("Mass must be a number")
        if mass <= 0:
            raise ValueError("Mass must be positive")
        self.__mass = mass

    def set_velocity(self, velocity):
        if not isinstance(velocity, vtkVector3d):
            raise TypeError("Velocity must be a vtkVector3d object")
        self.__velocity = velocity

    def get_mass(self):
        return self.__mass

    def get_velocity(self):
        return self.__velocity

    def set_gravity(self, bodies: list):
        currentVector = vtkVector3d(0, 0, 0)

        for body in bodies:
            if body is not self:

                dist_vect = vtkVector3d(body.get_position()[0] - self._position[0], body.get_position()[1] - self._position[1], body.get_position()[2] - self._position[2])
                unit_new_vector = dist_vect.Normalized()
                distance = dist_vect.Norm()
                scale_factor = self.GRAVITATIONAL_CONSTANT * (body.get_mass() * self.__mass) / (distance ** 2)
                new_vector = vtkVector3d(scale_factor * unit_new_vector[0], scale_factor * unit_new_vector[1], scale_factor * unit_new_vector[2])
                currentVector = vtkVector3d(currentVector[0] + new_vector[0], currentVector[1] + new_vector[1], currentVector[2] + new_vector[2])

        self.__gravity = currentVector

    def get_gravity(self):
        return self.__gravity

    #Methods
    def get_my_kinetic(self):
        return 0.5 * self.__mass * (self.__velocity.Norm() ** 2)

    def get_my_potential(self, bodies: list):
        potential_energy = 0
        for body in bodies:
            if body is not self:
                distance = (self._position - body.get_position()).Norm()
                potential_energy -= (self.GRAVITATIONAL_CONSTANT * self.__mass * body.get_mass()) / distance
        return potential_energy

    @staticmethod
    def get_system_kinetic(newtonianBodies: list):
        total_kinetic_energy = 0
        for body in newtonianBodies:
            if isinstance(body, NewtonianBody):
                total_kinetic_energy += body.get_my_kinetic()
        return total_kinetic_energy

    @staticmethod
    def get_system_potential(newtonianBodies: list):
        total_potential_energy = 0
        for i in range(len(newtonianBodies)):
            for j in range(i + 1, len(newtonianBodies)):
                if isinstance(newtonianBodies[i], NewtonianBody) and isinstance(newtonianBodies[j], NewtonianBody):
                    distance = (vm.add_vecs(newtonianBodies[i].get_position(), vm.scale_vec(-1, newtonianBodies[j].get_position()))).Norm()
                    total_potential_energy -= (NewtonianBody.GRAVITATIONAL_CONSTANT * newtonianBodies[i].get_mass() * newtonianBodies[j].get_mass()) / distance
        return total_potential_energy

    @staticmethod
    def get_system_energy(newtonianBodies: list):
        return NewtonianBody.get_system_kinetic(newtonianBodies) + NewtonianBody.get_system_potential(newtonianBodies)

