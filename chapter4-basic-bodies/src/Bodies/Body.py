from cmath import sqrt
from vtkmodules.vtkCommonDataModel import vtkVector3d

class Body:
    def __init__ (self, position, radius):
        self.__position = position
        self.__radius = radius


    #Getters and Setters
    def set_position(self, position):
        if not isinstance(position, vtkVector3d):
            raise TypeError("Position must be a vtkVector3d object")
        self.__position = position

    def set_radius(self, radius):
        if not isinstance(radius, (int, float)):
            raise TypeError("Radius must be a number")
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.__radius = radius

    def get_position(self):
        return self.__position

    def get_radius(self):
        return self.__radius

    #Methods
    def distanceSquared(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        distance_squared = (self.__position.GetX() - other_body.get_position().GetX()) ** 2 + \
                           (self.__position.GetY() - other_body.get_position().GetY()) ** 2 + \
                           (self.__position.GetZ() - other_body.get_position().GetZ()) ** 2
        return distance_squared

    def distance(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        return sqrt(self.distanceSquared(other_body))

    def doesIntersect(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        return self.distanceSquared(other_body) < (self.__radius + other_body.get_radius()) ** 2

    def isInBounds(self, bounds):
        if not isinstance(bounds, (list, tuple)) or len(bounds) != 6:
            raise TypeError("Bounds must be a list or tuple of length 6")
        x_min, x_max, y_min, y_max, z_min, z_max = bounds

        isInX = x_min <= self.__position.GetX() - self.__radius and self.__position.GetX() + self.__radius <= x_max
        isInY = y_min <= self.__position.GetY() - self.__radius and self.__position.GetY() + self.__radius <= y_max
        isInZ = z_min <= self.__position.GetZ() - self.__radius and self.__position.GetZ() + self.__radius <= z_max

        return isInX and isInY and isInZ


if __name__ == "__main__":
    #Test
    position1 = vtkVector3d(0, 0, 0)
    radius1 = 1
    body1 = Body(position1, radius1)

    position2 = vtkVector3d(1, 1, 1)
    radius2 = 1
    body2 = Body(position2, radius2)

    print("Distance squared:", body1.distanceSquared(body2))
    print("Distance:", body1.distance(body2))
    print("Do they intersect?", body1.doesIntersect(body2))

    bounds = [-2, 2, -2, 2, -2, 2]
    print("Is body1 in bounds?", body1.isInBounds(bounds))
    print("Is body2 in bounds?", body2.isInBounds(bounds))