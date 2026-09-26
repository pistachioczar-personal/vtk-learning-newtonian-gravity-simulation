from cmath import sqrt
from vtkmodules.vtkCommonDataModel import vtkVector3d

class Body:
    def __init__ (self, position: vtkVector3d, radius):
        self._position = position
        self._radius = radius


    #Getters and Setters
    def set_position(self, position: vtkVector3d):
        if not isinstance(position, vtkVector3d):
            raise TypeError("Position must be a vtkVector3d object")
        self._position = position

    def set_radius(self, radius):
        if not isinstance(radius, (int, float)):
            raise TypeError("Radius must be a number")
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self._radius = radius

    def get_position(self):
        return self._position

    def get_radius(self):
        return self._radius

    #Methods
    def distance_squared(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        distance_squared = (self._position.GetX() - other_body.get_position().GetX()) ** 2 + \
                           (self._position.GetY() - other_body.get_position().GetY()) ** 2 + \
                           (self._position.GetZ() - other_body.get_position().GetZ()) ** 2
        return distance_squared

    def distance(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        return sqrt(self.distance_squared(other_body))

    def does_intersect(self, other_body):
        if not isinstance(other_body, Body):
            raise TypeError("Argument must be a Body object")
        return self.distance_squared(other_body) < (self._radius + other_body.get_radius()) ** 2
    

    def is_in_bounds(self, bounds: list):
        if len(bounds) != 6:
            raise TypeError("Bounds must be a list of length 6")
        x_min, x_max, y_min, y_max, z_min, z_max = bounds
        isInX = x_min <= self._position.GetX() - self._radius and self._position.GetX() + self._radius <= x_max
        isInY = y_min <= self._position.GetY() - self._radius and self._position.GetY() + self._radius <= y_max
        isInZ = z_min <= self._position.GetZ() - self._radius and self._position.GetZ() + self._radius <= z_max

        return isInX and isInY and isInZ


if __name__ == "__main__":
    #Test
    position1 = vtkVector3d(0, 0, 0)
    radius1 = 1
    body1 = Body(position1, radius1)

    position2 = vtkVector3d(1, 1, 1)
    radius2 = 1
    body2 = Body(position2, radius2)

    print("Distance squared:", body1.distance_squared(body2))
    print("Distance:", body1.distance(body2))
    print("Do they intersect?", body1.does_intersect(body2))

    bounds = [-2, 2, -2, 2, -2, 2]
    print("Is body1 in bounds?", body1.is_in_bounds(bounds))
    print("Is body2 in bounds?", body2.is_in_bounds(bounds))