import matplotlib.pyplot as plot
from math import *
from tkinter import *

class Rocket(object):
    def __init__(self, when, x, y, vy, vx, mr, mp, c, F, angle, mz,  G = 6.67*10**-11):
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
        self.when = when
        self.time = 0
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
        "direction" : [],
        "specials x" : [],
        "specials y" : []
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
            self.time += 1
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


def velangle_to_xy(velocity, angle):
    x = velocity * sin(radians(angle))
    y = velocity * cos(radians(angle))
    return[x, y]


def xy_to_velangle(velx, vely):
    veltotal = sqrt(velx**2 + vely**2)
    angle = degrees(atan2(velx, vely))
    return [veltotal, angle]


def rgbtohex(r, g, b):
    val = ""
    rhex = str(hex(int(str(r)))[2:])
    ghex = str(hex(int(str(g)))[2:])
    bhex = str(hex(int(str(b)))[2:])
    if r <= 16:
        rhex = str("0" + rhex)
    if g <= 16:
        ghex = (str("0" + ghex))
    if b <= 16:
        bhex = (str("0" + bhex))
    val = str(rhex) + str(ghex) + str(bhex)
    return val


def path(rocket):
    size = 0
    size = sorted(rocket.history["distance to body"], reverse = True)[0]
    size *= 1.2
    plot.plot(sphere(6378000)[0], sphere(6378000)[1])
    plot.scatter(rocket.x, rocket.y)
    max_velocity = sorted(rocket.history["total velocity"], reverse = True)[0]
    color = []
    for i in range(len(rocket.history["total velocity"])):
        r = int((rocket.history["total velocity"][i] / max_velocity) * 256)
        color.append(r)
    plot.scatter(rocket.history["specials x"], rocket.history["specials y"], c = "red" )
    plot.scatter(rocket.history["x"], rocket.history["y"], s = 1, c = color)
    plot.xlim(-size, size)
    plot.ylim(-size, size)
    plot.ylabel("")
    plot.show()


def stage(previous, next):
    if isinstance(next.x, int):
        next.x = previous.x
    if isinstance(next.y, int):
        next.y = previous.y
    if isinstance(next.vy, int):
        next.vy = previous.vy
    if isinstance(next.vx, int):
        next.vx = previous.vx
    if isinstance(next.mr, int):
        next.mr = previous.mr
    if isinstance(next.mp, int):
        next.mp = previous.mp
    if isinstance(next.c, int):
        next.c = previous.c
    if isinstance(next.F, int):
        next.F = previous.F
    if isinstance(next.angle, int):
        next.angle = previous.angle
    if isinstance(next.mz, int):
        next.mz = previous.mz
    return next


def sphere(r):
    x = []
    y = []
    for i in range(360):
        x.append(sin(radians(i)) * r)
        y.append(cos(radians(i)) * r)
    return [x,y]

def renew_rocket_window():
    try:
        Rocket_window.quit()
    except NameError:
        pass
    Stage_submit.quit()

def read_entries(values):
    return Rocket(
        values[0],
        values[1],
        values[2],
        values[3],
        values[4],
        values[5],
        values[6],
        values[7],
        values[8],
        values[9],
        values[10],
    )

def main(rocket, draw_time):
    while True:
        for i in range(draw_time):
            rocket.update()
            if sqrt(rocket.x**2 + rocket.y **2) < 6378000:
                path(rocket)
                return
        path(rocket)

default = Rocket(
"start",
0,       #x
6378000, #y
0,       #velocity y
600,     #velocity x
5000,     #mass of hull
0,       #mass of fuel
1,      #consumption
90000,  #engine force
0,       #angle
6*10**24#mass of body
)

Stage_submit = Tk()
Label(Stage_submit, text = "Amount of stages ").grid(row = 0, column = 0)
stage_entry = Entry(Stage_submit)
stage_entry.grid(row = 0, column = 1)
Button(Stage_submit, text = "Submit", command = Stage_submit.quit).grid(row = 1, column = 0)
Button(Stage_submit, text = "Exit", command = Stage_submit.destroy).grid(row = 1, column = 1)
Stage_submit.mainloop()
stage_amount = int(stage_entry.get())
Stage_submit.destroy()

Rocket_window = Tk()
Label(Rocket_window, text = "").grid(row = 0, column = 0)
Label(Rocket_window, text = "When?").grid(row = 1, column = 0)
Label(Rocket_window, text = "Location x").grid(row = 2, column = 0)
Label(Rocket_window, text = "Location y", pady = 3).grid(row = 3, column = 0)
Label(Rocket_window, text = "Vertical velocity", pady = 3).grid(row = 4, column = 0)
Label(Rocket_window, text = "Horizontal velocity", pady = 3).grid(row = 5, column = 0)
Label(Rocket_window, text = "Mass of hull", pady = 3).grid(row = 6, column = 0)
Label(Rocket_window, text = "Amount of fuel", pady = 3).grid(row = 7, column = 0)
Label(Rocket_window, text = "Fuel consumption", pady = 3).grid(row = 8, column = 0)
Label(Rocket_window, text = "Engine force", pady = 3).grid(row = 9, column = 0)
Label(Rocket_window, text = "Angle of thrust", pady = 3).grid(row = 10, column = 0)
Label(Rocket_window, text = "Mass of gravitational body", pady = 3).grid(row = 11, column = 0)

stage_parameters_list = []
for i in range(stage_amount):
    Label(Rocket_window, text = "stage " + str(i)).grid(row = 0, column = i + 1)
    stage_parameters = []
    for ii in range(11):
        stage_parameters.append(Entry(Rocket_window))
        stage_parameters[ii].grid(row = ii + 1, column = i + 1)
    stage_parameters_list.append(stage_parameters)
    print(stage_parameters)

Button(Rocket_window, command = Rocket_window.quit, text = "show").grid(row = 12, column = 1)
stage_parameters_list[0][0].insert(0, default.when)
stage_parameters_list[0][1].insert(0,default.x)
stage_parameters_list[0][2].insert(0,default.y)
stage_parameters_list[0][3].insert(0,default.vy)
stage_parameters_list[0][4].insert(0,default.vx)
stage_parameters_list[0][5].insert(0,default.mr)
stage_parameters_list[0][6].insert(0,default.mp)
stage_parameters_list[0][7].insert(0,default.c)
stage_parameters_list[0][8].insert(0,default.F)
stage_parameters_list[0][9].insert(0,default.angle)
stage_parameters_list[0][10].insert(0,default.mz)






Rocket_window.mainloop()
main(read_entries(stage_parameters_list[0]))
