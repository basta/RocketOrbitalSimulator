import matplotlib.pyplot as plot
from math import *
# v = 0
# mr = 1000
# mp = 100
# def mt():
#     return mp + mr
# mz = 6 * 10**24
# r = 6378000
# h = 0
# def d():
#     return r + h
# c = 10
# F = 200000
# G = 6.67 * 10**-11
# def g():
#     return (G * mz)/d()**2
# def a():
#     return F / mt()
# velocity, fuel, height, gravity, acceleration, total_a = [], [], [], [], [], []

class Rocket(object):
    def __init__(self, x, y, vy, vx, mr, mp, mz, c, F, angle, G = 6.67*10**-11):
        self.vx = vx
        self.vy = vy
        self.mr = mr
        self.mp = mp
        self.mz = mz
        self.x = x
        self.y = y
        self.c = c
        self.F = F
        self.G = G
        self.vt = sqrt(vx**2 + vy**2)
        self.mt = mr + mp
        self.d = sqrt(x**2 + y**2)
        self.g = (self.G * self.mz)/self.d**2
        self.ax = (F / self.mt) * sin(radians(angle))
        self.ay = (F / self.mt) * cos(radians(angle))
        self.at = sqrt(self.ax**2 + self.ay**2)
        self.angle = angle
        self.height = self.d - 6378000
        self.relevant_vals = [self.vy, self.vx, self.mr, self.mp, self.mz, self.x, self.y,
            self.c, self.F, self.vt, self.mt, self.d, self.g, self.ax, self.ay,
            self.at, self.angle, self.height]
        self.history = {
        "vertical velocity" : [],
        "horizontal velocity" : [],
        "rocket mass" : [],
        "fuel mass" : [],
        "mass of pulling body" : [],
        "x" : [],
        "y" : [],
        "fuel consumption" : [],
        "engine force" : [],
        "total velocity" : [],
        "total mass" : [],
        "distance to body" : [],
        "gravity force" : [],
        "horizontal acceleration" : [],
        "vertical acceleration" : [],
        "total acceleration" : [],
        "angle" : [],
        "height" : [],
        "direction" : []
        }

    def save(self):
        names = ["vertical velocity", "horizontal velocity", "rocket mass", "fuel mass",
        "mass of pulling body", "x", "y", "fuel consumption", "engine force",
        "total velocity", "total mass", "distance to body", "gravity force",
        "horizontal acceleration", "vertical acceleration", "total acceleration",
        "angle", "height"]
        for i in range(len(names)):
            self.history[names[i]].append(self.relevant_vals[i])
        self.history["direction"].append(self.direction)

    def location(self):
        return([self.x, self.y])

    def update(self):
            if self.mp <= 0:
                self.F = 0
                self.c = 0
            self.vt = sqrt(self.vx**2 + self.vy**2)
            self.vx = self.vx + self.ax
            self.vy = self.vy + self.ay
            self.mt = self.mr + self.mp
            self.g = (self.G * self.mz)/self.d**2
            self.a = self.F/self.mt
            self.ax = (self.F / self.mt) * sin(radians(self.angle))
            self.ay = (self.F / self.mt) * cos(radians(self.angle))
            self.at = sqrt(self.ax**2 + self.ay**2)
            self.x += self.vx
            self.y += self.vy
            self.d = sqrt(self.x**2 + self.y**2)
            self.direction = degrees(atan2(self.x, self.y))
            print(self.direction)
            self.vx += -sin(radians(self.direction)) * self.g
            self.vy += -cos(radians(self.direction)) * self.g
            self.mp += -self.c
            self.save()
            print("Height: " + str(self.d - 6378000) + "m \n",
            "Velocity: " + str(sqrt(self.vy**2 + self.vx**2)) + " m/s \n",
            "Acceleration: " + str(self.at) + " m/s/s \n",
            "Gravity: " + str(self.g) + " m/s/s \n",
            "Fuel: " + str(self.mp) + " kg \n",
            "Direction: " + str(self.history["direction"][-1]) + "\n")
            self.relevant_vals = [self.vy, self.vx, self.mr, self.mp, self.mz, self.x, self.y,
                self.c, self.F, self.vt, self.mt, self.d, self.g, self.ax, self.ay,
                self.at, self.angle, self.height]

    def turn(angle):
        self.angle += angle


def path(rocket):
    size = 0
    size = sorted(rocket.history["distance to body"], reverse = True)[0]
    size *= 1.2
    plot.plot(sphere(6378000)[0], sphere(6378000)[1])
    plot.plot(rocket.history["x"], rocket.history["y"])
    plot.xlim(-size, size)
    plot.ylim(-size, size)
    plot.ylabel("")
    plot.show()


def sphere(r):
    x = []
    y = []
    for i in range(360):
        x.append(sin(radians(i)) * r)
        y.append(cos(radians(i)) * r)
    return [x,y]


def main(rocket):
    while True:
        for i in range(1000):
            rocket.update()
            if sqrt(rocket.x**2 + rocket.y **2) < 6378000:
                path(rocket)
                return
        path(rocket)


default = Rocket(
0,       #x
6678000, #y
0,       #velocity y
8000, #velocity x
500,     #mass of hull
0,       #mass of fuel
6*10**24,#mass of body
20,      #consumption
60000,  #engine force
0       #angle
)


main(default)
