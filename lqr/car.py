import math
from numpy import random
import numpy as np

class Car:
    def __init__(self, x=0, y=0, vx=0, vy=0, dt=.05):
        self.x = np.array([x , y, vx, vy]) #x, y, vx, vy
        self.u = np.array([0, 0]) #ax, ay
        self.previous_positions = []
        self.width = 30
        self.height = 50
        self.thrust = 200
        self.dt = dt
        self.A = np.array([[1, 0, dt, 0], 
              [0, 1, 0, dt],
              [0, 0, (1-dt), 0],
              [0, 0, 0, (1-dt)]])

        self.B = np.array([[0, 0],
              [0, 0],
              [self.thrust*dt, 0],
              [0, self.thrust*dt]])

    def update(self):
        self.x = self.A@self.x + self.B@self.u
        
