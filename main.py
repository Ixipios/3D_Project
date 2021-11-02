import turtle
from math import sqrt, sin, cos
import math
from time import sleep
import keyboard
from random import randint

turtle.hideturtle()
turtle.tracer(0, 0)
turtle.pensize(2)

render_distance = 150


class Vec:
    def __init__(self, x, y,z):
        self.x = x
        self.y = y
        self.z = z


def vector_sum(u, v):
    return Vec(u.x+v.x, u.y+v.y, u.z+v.z)


def vector_dif(u, v):
    return Vec(u.x-v.x, u.y-v.y, u.z-v.z)


class Droite:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def create_droite(self, A, B):
        xa, ya, za = A
        xb, yb, zb = B
        if sqrt(xa**2+ya**2+za**2) > sqrt(xb**2+yb**2+zb**2):
            direction_vector = Vec(xa-xb, ya-yb, za-zb)
        else:
            direction_vector = Vec(xb-xa, yb-ya, zb-za)
        # print(direction_vector.x, direction_vector.y, direction_vector.z)
        self.x = xa, direction_vector.x
        self.y = ya, direction_vector.y
        self.z = za, direction_vector.z


def is_point_visible(point, lens_point):
    if point[2] <= lens_point[2] or point[2] >= render_distance:
        return False
    return True


def is_cube_visible(cube, lens_point):
    visible = False
    for point in cube:
        if is_point_visible(point, lens_point):
            visible = True
    return visible


class World:
    def __init__(self, cubes, lens_point):
        self.cubes = cubes
        self.lens_point = lens_point

    def move(self, vector: Vec):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i])):
                point = self.cubes[i][j]
                self.cubes[i][j] = (point[0]+vector.x, point[1]+vector.y, point[2]+vector.z)

    def draw(self):
        for cube in self.cubes:
            if is_cube_visible(cube, self.lens_point):
                cube_3d_to_2d(cube, self.lens_point)
        turtle.update()
        sleep(0.01)
        turtle.clear()


def projection(A, B):
    """
    Projete un point sur un plan en passant par un point-lentille
    :param A: le point a projeté sur le plan (vec_i, vec_j) du repère
    :param B: le point-lentille
    :return: un point, la projection de A sur le plan
    """
    d = Droite(0, 0, 0)
    d.create_droite(A, B)
    # print("d:", d.x, d.y, d.z)
    if d.z[1] != 0:
        t = (-d.z[0]) / d.z[1]
    else:
        t = 0
    # print(t)
    C = (d.x[0] + d.x[1] * t, d.y[0] + d.y[1] * t) # the projection
    # print(C)
    return C


def draw_point(p):
    turtle.penup()
    turtle.goto(p)
    turtle.pendown()
    turtle.fd(1)
    # turtle.update()


def draw_line(A, B):
    turtle.penup()
    turtle.goto(A)
    turtle.pendown()
    turtle.goto(B)
    # turtle.update()


def draw_cube(points):
    for i in range(3):
        draw_line(points[i], points[i+1])
    draw_line(points[3], points[0])
    draw_line(points[0], points[4])
    for i in range(4, 7):
        draw_line(points[i], points[i+1])
    draw_line(points[7], points[4])
    draw_line(points[5], points[1])
    draw_line(points[6], points[2])
    draw_line(points[7], points[3])


def create_cube(A, l):
    points = [A, (A[0]+l, A[1], A[2]), (A[0]+l, A[1]+l, A[2]), (A[0], A[1]+l, A[2]),
              (A[0], A[1], A[2]+l), (A[0]+l, A[1], A[2]+l), (A[0]+l, A[1]+l, A[2]+l), (A[0], A[1]+l, A[2]+l)]
    return points


def rotation(cube):
    precision = 10**2
    zoom = 1
    new_cube = [0]*8
    for i in range(2*314):
        i = i/precision
        print("new_cube", new_cube)
        cube_to_draw = []
        for j in range(len(cube)//2):
            print("sin", sin(i/100+(math.pi/2)*j))
            new_cube[j] = (zoom*cos(i+math.pi/2*j), zoom*sin(i+math.pi/2*j), 0)
            new_point = projection([new_cube[j][0]+cube[j][0], new_cube[j][1]+cube[j][1], new_cube[j][2]+cube[j][2]], lens_point)
            cube_to_draw.append((new_point[0]*-1000000, new_point[1]*-1000000))
        print(len(cube)//2, len(cube))
        for j in range(len(cube)//2, len(cube)):
            print("sin", sin(i + (math.pi / 2)*(j-len(cube)//2)))
            new_cube[j] = (zoom*cos(i+(math.pi/2)*(j-len(cube)//2)), zoom*sin(i+(math.pi/2)*(j-len(cube)//2)), 0)
            new_point = projection([new_cube[j][0]+cube[j][0], new_cube[j][1]+cube[j][1], new_cube[j][2]+cube[j][2]], lens_point)
            cube_to_draw.append((new_point[0]*-1000000, new_point[1]*-1000000))
        print("cube_to_draw", len(cube_to_draw), cube_to_draw)
        draw_cube(cube_to_draw)
        turtle.update()
        sleep(0.01)
        turtle.clear()


def rotation_point(point, alpha, axis):
    radius = 0


def cube_3d_to_2d(cube1, lens_point1):
    cube2 = []
    for i in cube1:
        # print(cube1)
        # print("i:", i)
        p = projection(i, lens_point1)
        # print(p)
        cube2.append((p[0] * -1000000, p[1] * -1000000))
        # print(cube2)
    draw_cube(cube2)


def rotation_mouse(world):
    precision = 10
    zoom = 1
    for i in range(31, 3*31):
        i = i / precision
        world.move(Vec(zoom*cos(i), 0, zoom*sin(i)))
        world.draw()


def game_0(cube1):
    """
    1 cube world
    :param cube1:
    :return:
    """
    speed = 0.8
    lens_point1 = (0, 0, 0.001)
    sneak = 1
    while 1:
        if keyboard.is_pressed("d"):
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0]-speed, cube1[i][1], cube1[i][2])
        if keyboard.is_pressed("q"):
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0]+speed, cube1[i][1], cube1[i][2])
        if keyboard.is_pressed("z"):
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0], cube1[i][1], cube1[i][2]-speed)
        if keyboard.is_pressed("s"):
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0], cube1[i][1], cube1[i][2]+speed)
        """
        if keyboard.read_key() == "ctrl":
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0], cube1[i][1]-speed*sneak, cube1[i][2])
            sneak *= -1
        """
        if keyboard.is_pressed(" "):
            for x in range(-10, 0):
                for i in range(len(cube1)):
                    cube1[i] = (cube1[i][0], cube1[i][1] - ((-x/5)**2/4), cube1[i][2])
                cube_3d_to_2d(cube1)
            # sleep(0.06)
            for x in range(11):
                for i in range(len(cube1)):
                    cube1[i] = (cube1[i][0], cube1[i][1] + ((-x/5)**2/4), cube1[i][2])
                cube_3d_to_2d(cube1)
        else:
            cube_3d_to_2d(cube1)


def game_1(world):
    """
    multi-cubes world
    :return:
    """
    speed = 0.5
    lens_point1 = [0, 0, 0.001]
    sneak = 1
    while 1:
        if keyboard.is_pressed("e"):
            lens_point1[2] -= 0.0001
            world.lens_point = lens_point1
        if keyboard.is_pressed("t"):
            lens_point1[2] += 0.0001
            world.lens_point = lens_point1
        if keyboard.is_pressed("d"):
            world.move(Vec(-1, 0, 0))
        if keyboard.is_pressed("q"):
            world.move(Vec(1, 0, 0))
        if keyboard.is_pressed("z"):
            world.move(Vec(0, 0, -1))
        if keyboard.is_pressed("s"):
            world.move(Vec(0, 0, 1))
        """
        if keyboard.read_key() == "ctrl":
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0], cube1[i][1]-speed*sneak, cube1[i][2])
            sneak *= -1
        """
        if keyboard.is_pressed(" "):
            for x in range(-10, 0):
                world.move(Vec(0, - ((-x / 5) ** 2 / 4), 0))
                world.draw()
            # sleep(0.06)
            for x in range(11):
                world.move(Vec(0, (-x / 5) ** 2 / 4, 0))
                world.draw()
        else:
            world.draw()


def random_gen(n_cubes, lens_point1):
    cubes = []
    for i in range(n_cubes):
        cubes.append(create_cube((randint(-10, 10), randint(-10, 10), randint(-100, 500)), 2))
    return World(cubes, lens_point1)


lens_point = (0, 0, 0.001)
cube0 = create_cube((-8, -4, 20), 2)
cube2 = create_cube((10, -4, 20), 2)
world1 = World([cube0, cube2, create_cube((-8, -2, 20), 2), create_cube((-2, -6, 20), 2), create_cube((-2, -6, 200), 2),
                create_cube((8, -6, 250), 2)], lens_point)
# print(cube0)
# print(len(cube0))
cube_2d = []
"""
for i in cube:
    print(cube)
    print("i:", i)
    p = projection(i, lens_point)
    print(p)
    cube_2d.append((p[0]*-1000000, p[1]*-1000000))
    print(cube_2d)
    draw_cube(cube_2d)
"""

draw_point((0, 0))
# game_0(cube0)
game_1(random_gen(20, lens_point))
# rotation_mouse(world1)

"""
for a in range(9, 90):
    cube = create_cube((a, 0, a), 13)
    for i in cube:
        print("i:", i)
        p = projection(i, lens_point)
        cube_2d.append((p[0]*-10, p[1]*-10))
    draw_cube(cube_2d)
    cube_2d = []
    sleep(0.001)
    turtle.clear()
"""
print(cube_2d)

turtle.mainloop()
