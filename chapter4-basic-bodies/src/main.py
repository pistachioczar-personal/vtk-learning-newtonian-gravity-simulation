from bodies import NewtonianBody
import math

def main(number_of_bodies):

    bodies = [NewtonianBody() for _ in range(number_of_bodies)]

    max_radius = max_radius(number_of_bodies, 0.1, 1.0)

def max_radius(number_of_bodies: int, ratio: float, volume: float):
    if ratio > 1 or ratio <= 0:
        raise ValueError("Ratio must be a positive float less than or equal to 1")
    max_radius = ratio/2 * (volume / number_of_bodies) ** (1/3)
    return max_radius
