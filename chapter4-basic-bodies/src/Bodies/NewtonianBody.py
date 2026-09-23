import Body
from typing import Final
from vtkmodules.vtkCommonDataModel import vtkVector3d

class NewtonianBody(Body):
    def __init__(self, position, radius, velocity, gravity, mass):
        super().__init__(position, radius)
        self.__mass = mass
        self.__velocity = velocity
        self.__gravity = gravity
        self.GRAVITATIONAL_CONSTANT: Final = 0.000295913120346


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
                unitNewVector = (body.get_position() - self.__position).Normalized()
                distance = (body.get_position() - self.__position).Norm()
                newVector = unitNewVector * (-self.GRAVITATIONAL_CONSTANT * (body.get_mass() * self.__mass) / (distance ** 2))
                currentVector += newVector

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
                distance = (self.__position - body.get_position()).Norm()
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
    def get_system_potential(newtonianBodies: list, self):
        total_potential_energy = 0
        for i in range(len(newtonianBodies)):
            for j in range(i + 1, len(newtonianBodies)):
                if isinstance(newtonianBodies[i], NewtonianBody) and isinstance(newtonianBodies[j], NewtonianBody):
                    distance = (newtonianBodies[i].get_position() - newtonianBodies[j].get_position()).Norm()
                    total_potential_energy -= (self.GRAVITATIONAL_CONSTANT * newtonianBodies[i].get_mass() * newtonianBodies[j].get_mass()) / distance
        return total_potential_energy

    @staticmethod
    def get_system_energy(self, newtonianBodies: list):
        return self.get_system_kinetic(newtonianBodies) + self.get_system_potential(newtonianBodies, self)

    
    
    
