## Description

A 3D Newtonian N-body simulation built in Python. This project uses VTK to render a randomly generated system of celestial bodies, visualizing their initial velocity vectors and the resulting gravitational pull between them. This is going to do the same thing as last chapters with small changes that I will describe after the system defaults and their derived constants which are carried over from chapter 4.

### System Defaults

- Unit of Mass = 1 solar mass (1.988,416 \* 10^30 kg)
- Unit of Distance = 1 Astronomical Unit (149,597,870,700 meters)
- Unit of Time = 1 Day (86,400 seconds)

### Derived Constants From Defaults

- Unit of Energy = [(Solar mass) * (AU)^2 ] / (Day)^2
- Gravitational Constant = 0.000295913120346

## Planned Changes

Chapter 4's project was a rough coding of the simulation. In this version I will optimize my code to run faster and cleaner. To achieve this I will utilize NumPy vectorizations, unit testing and an added class that holds the system as a whole. I will implement unit testing to ensure my previous methods and calculations are accurate, this will also allow me to modularize my code more concisely. While I already implemented some chapter 5 concepts I will be adding imagedata to form a 3D grid, making the perspective of the system easier to understand. I will also use vtkFieldData
