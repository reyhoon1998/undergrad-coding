import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Atom:
    def __init__(self, theta0):
        self.theta0 = theta0

    def move(self,walk_size):
        random_phase = random.random()
        if random_phase > 0.5:
            self.theta0 += walk_size
            if self.theta0 > 360:
                self.theta0 -= 360
        else:
            self.theta0 -= walk_size
            if self.theta0 < 1:
                self.theta0 += 360

    def get_location(self, radius):
        return [(radius * np.cos((self.theta0 * 2 * np.pi / 360))), radius * np.sin((self.theta0 * 2 * np.pi / 360))]


print("First Atom Degree (integer from 0 to 360) Input:")
atom1 = Atom(int(input()))

print("SecondAtom Degree (integer from 0 to 360) Input:")
atom2 = Atom(int(input()))
radius = 40

walk_size = 10

if atom1.theta0 > atom2.theta0:
    temp = atom1
    atom1 = atom2
    atom2 = temp

fig = plt.figure()
point1, = plt.plot([atom1.get_location(radius)[0]], [atom1.get_location(radius)[1]], "X")
point2, = plt.plot([atom2.get_location(radius)[0]], [atom2.get_location(radius)[1]], "X")


def draw_circle():
    theta = np.linspace(0, 2 * np.pi, 500)
    a = radius * np.cos(theta)
    b = radius * np.sin(theta)
    plt.axis([-radius*2, radius*2, -radius*2, radius*2])
    plt.plot(a, b)


def update(frame):
    atom1.move(walk_size)
    point1.set_data([atom1.get_location(radius)[0]], [atom1.get_location(radius)[1]])
    atom2.move(walk_size)
    point2.set_data([atom2.get_location(radius)[0]], atom2.get_location(radius)[1])
    frame += 1
    if atom2.theta0 <= atom1.theta0 and atom1.theta0 - atom2.theta0 <= walk_size:
        print("done in step : ", frame + 1)
        print("Atom 1 : ", atom1.theta0, chr(176), atom1.get_location(radius))
        print("Atom 2 : ", atom2.theta0, chr(176), atom2.get_location(radius))
        stop()


draw_circle()
animation = FuncAnimation(fig, update, interval=500)


def stop():
    animation._stop()


plt.show()