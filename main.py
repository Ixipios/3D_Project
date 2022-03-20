import turtle
from math import sqrt, sin, cos, acos, asin
import math
from time import sleep
import keyboard
from pynput import mouse
from pynput import keyboard as keyboard2
from random import randint

turtle.hideturtle()
turtle.tracer(0, 0)
turtle.pensize(1)

render_distance = 200

mouse = mouse.Controller()
kb = keyboard2.Controller()


class Vec:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.norm = sqrt(x**2+y**2+z**2)

    def __int__(self, p1, p2):
        self.x = p2[0]-p1[0]
        self.y = p2[1]-p1[1]
        self.z = p2[2]-p1[2]
        self.norm = sqrt(self.x**2+self.y**2+self.z**2)


def create_vec(A, B):
    return Vec(A[0]-B[0], A[1]-B[1], A[2]-B[2])


def vector_sum(u, v):
    return Vec(u.x+v.x, u.y+v.y, u.z+v.z)


def vector_dif(u, v):
    return Vec(u.x-v.x, u.y-v.y, u.z-v.z)


def vector_real_mult(u, k):
    return Vec(k*u.x, k*u.y, k*u.z)


def dot_product(u, v):
    return u.x*v.x + u.y*v.y + u.z*v.z


def get_columns(A):
    A_columns = []
    for i in range(len(A)-1):
        A_column = []
        for line in A:
            A_column.append(line[i])
        A_columns.append(A_column)
    return A_columns


def column_line_sum(c, l):
    if len(c) == len(l):
        sum = 0
        for i in range(len(c) - 1):
            sum += c[i] * l[i]
    else:
        return 0


def matrix_multiplication(A, B):
    result = []
    columns_B = get_columns(B)
    for i in range(len(A)-1):
        line = []
        sum = 0
        for j in range(len(A[i])-1):
            sum += A[i][j]*columns_B[i][j]
        line.append(sum)
    return result


class Droite:
    def __init__(self, point, direction_vector):
        self.point = point
        self.direction_vector = direction_vector

    # vecteur directeur --> un vecteur unitaire
    def create_droite(self, A, B):
        xa, ya, za = A
        xb, yb, zb = B
        if sqrt(xa**2+ya**2+za**2) > sqrt(xb**2+yb**2+zb**2):
            direction_vector = Vec(xa-xb, ya-yb, za-zb)
        else:
            direction_vector = Vec(xb-xa, yb-ya, zb-za)
        k = 1 / direction_vector.norm
        direction_vector = vector_real_mult(direction_vector, k)
        # print(direction_vector.x, direction_vector.y, direction_vector.z)
        self.point = (xa, ya, za)
        self.direction_vector = (direction_vector.x, direction_vector.y, direction_vector.z)


class Plan:
    def __init__(self, origin, normal_vector: Vec):
        # a point that defines the plan
        self.origin = origin
        # two vectors that define the plan
        self.normal_vector = normal_vector

    def create(self, A, B, C):
        self.vec1 = create_vec(A, B)
        self.vec2 = create_vec(A, C)
        self.point(A)


def is_point_visible(point, lens_point):
    if point[1] <= lens_point[1] or point[1] >= render_distance:
        return False
    return True


def is_cube_visible(cube, lens_point):
    visible = True
    for point in cube.points:
        if not is_point_visible(point, lens_point):
            visible = False
    return visible


def orthogonal_projection(point, plane: Plan):
    """
    Project a point on a given plan
    :param point: the point to project on the plan
    :param plane: the plan to project the point on
    :return: the projection (a point as a tuple) of the point on the plane
    """
    # look to the photos for more explanation
    d = Droite(point, plane.normal_vector)
    vec = Vec(point, plane.origin)
    t = dot_product(vec, plane.normal_vector) / plane.normal_vector.norm
    return plane.normal_vector.x * t + point[0], plane.normal_vector.y * t + point[1], plane.normal_vector.z * t + point[2]


def cube_equation(cube):
    pass


class Cube:
    def __init__(self, points):
        self.points = points
        d1 = Droite(0, 0)
        d2 = Droite(0, 0)
        d1.create_droite(points[0], points[6])
        print(d1.point, d1.direction_vector)
        d2.create_droite(points[1], points[7])
        t = 0
        x1, y1, z1 = d1.point
        x2, y2, z2 = d2.point
        a1, b1, c1 = d1.direction_vector
        a2, b2, c2 = d2.direction_vector
        if x1 != x2:
            t = (x1-x2)/(a2-a1)
        elif y1 != y2:
            t = (y1-y2)/(b2-b1)
        else:
            t = (z1-z2)/(c2-c1)
        self.center = (x1+a1*t, y1+b1*t, z1+c1*t)


class World:
    def __init__(self, cubes, lens_point):
        self.cubes = cubes
        self.lens_point = lens_point

    def draw(self):
        for cube in self.cubes:
            if is_cube_visible(cube, self.lens_point):
                cube_3d_to_2d(cube, self.lens_point)
        turtle.update()
        sleep(0.01)
        turtle.clear()

    def move(self, vector: Vec):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i].points)):
                point = self.cubes[i].points[j]
                self.cubes[i].points[j] = (point[0]+vector.x, point[1]+vector.y, point[2]+vector.z)

    def rotate(self, theta, axis):
        for cube in self.cubes:
            rotate_cube(cube, theta, axis)


def projection(A, B):
    """
    Projete un point sur un plan en passant par un point-lentille
    :param A: le point a projeté sur le plan (vec_i, vec_j) du repère
    :param B: le point-lentille
    :return: un point, la projection de A sur le plan
    """
    d = Droite(0, 0)
    d.create_droite(A, B)
    # print("d:", d.x, d.y, d.z)
    if d.direction_vector[1] != 0:
        t = (-d.point[1]) / d.direction_vector[1]
    else:
        t = 0
    # print(t)
    C = (d.point[0] + d.direction_vector[0] * t, d.point[2] + d.direction_vector[2] * t)  # the projection
    # print(C)
    return C


def projection_general(A, P):
    """
    Project a given point of the 3d-space on a given plan
    :return: the coordinates of the projection of A on P
    """
    # find the coordinates of the intersection


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


def project_line(A, B, lens_point):
    new_A = projection(A, lens_point)
    new_B = projection(B, lens_point)
    draw_line(new_A, new_B)


def project_cube(cube, lens_point):
    cube_projection = []
    for point in cube.points:
        point_projection = projection(point, lens_point)
        cube_projection.append((point_projection[0] * -1000000, point_projection[1] * -1000000))
    return cube_projection


def create_cube(A, l):
    points = [A, (A[0]+l, A[1], A[2]), (A[0]+l, A[1], A[2]+l), (A[0], A[1], A[2]+l),
              (A[0], A[1]+l, A[2]), (A[0]+l, A[1]+l, A[2]), (A[0]+l, A[1]+l, A[2]+l), (A[0], A[1]+l, A[2]+l)]
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


def rotation2(cube):
    precision = 100
    zoom = 4*sqrt(5)
    new_cube = [0] * 8
    for i in range(2 * 314):
        i = i / precision
        cube_to_draw = []
        for j in range(len(cube)):
            new_cube[j] = (zoom * cos(i), 0, zoom * sin(i))
            new_point = projection(
                [new_cube[j][0] + cube[j][0], new_cube[j][1] + cube[j][1], new_cube[j][2] + cube[j][2]], lens_point)
            cube_to_draw.append((new_point[0] * -1000000, new_point[1] * -1000000))
        draw_cube(cube_to_draw)
        turtle.update()
        sleep(0.01)
        turtle.clear()


def rotate_point(point, theta, axis: Droite):
    """ Pour rotations particulières
    xa, ya, za = point  # the point coordinates
    a, b, c = axis.x[1], axis.y[1], axis.z[1]  # the coefficients of the axis equation
    xb, yb, zb = axis.x[0], axis.y[0], axis.z[0]  # the point coordinates of the axis equation
    d = -a*xa - b*ya - c*za  # the d of the Cartesian equation of the plan: ax + by + cz + d = 0
    t = (-a*xb - b*yb - c*zb - d)/(a**2 + b**2 + c ** 2)  # the variable of the parametric equation of the axis
    xi, yi, zi = (xb + a*t, yb + b*t, zb + c*t)  # I is the point of intersection between the axis and the plan
    radius = sqrt((xa-xi)**2 + (ya-yi)**2 + (za-zi)**2)
    alpha = acos((xa - xi)/radius) + alpha
    new_point = (radius * cos(alpha) + xi, yi, radius * sin(alpha) + zi)
    print(new_point)
    print(xi, yi, zi)
    return new_point
    """
    # rotation générale
    point1 = (point[0]-axis.point[0], point[1]-axis.point[1], point[2]-axis.point[2])
    x, y, z = axis.direction_vector  # the coefficients of the axis equation
    d, e, f = point1
    c = cos(theta)
    c1 = 1-c
    s = sin(theta)
    # matrice de rotation
    rotation_matrix = [[(x**2)*c1+c, x*y*c1-z*s, x*z*c1+y*s],
                       [x*y*c1+z*s, (y**2)*c1+c, y*z*c1-x*s],
                       [x*z*c1-y*s, y*z*c1+x*s, (z**2)*c1+c]]
    # matrice sous forme mais représente bien une colone de coordonnées
    new_point = [d*rotation_matrix[0][0]+e*rotation_matrix[0][1]+f*rotation_matrix[0][2]+axis.point[0],
                 d*rotation_matrix[1][0]+e*rotation_matrix[1][1]+f*rotation_matrix[1][2]+axis.point[1],
                 d*rotation_matrix[2][0]+e*rotation_matrix[2][1]+f*rotation_matrix[2][2]+axis.point[2]]
    return new_point


def rotate_cube(cube, theta, axis):
    new_points = []
    for point in cube.points:
        new_points.append(rotate_point(point, theta, axis))
    cube.points = new_points


def rotation_cube(cube, alpha, axis):
    new_cube = []
    for point in cube:
        new_cube.append(rotate_point(point, alpha, axis))
    print(new_cube)
    return new_cube


def cube_3d_to_2d(cube1: Cube, lens_point1):
    cube2 = []
    for i in cube1.points:
        # print(cube1)
        # print("i:", i)
        p = projection(i, lens_point1)
        # print(p)
        cube2.append((p[0] * -1000000, p[1] * -1000000))
        # print(cube2)
    draw_cube(cube2)


def rotation_mouse(world):
    while 1:
        if keyboard.is_pressed("q"):
            world.rotate(math.pi/50, -1)
        if keyboard.is_pressed("d"):
            world.rotate(math.pi/50, 1)
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
    mouse_pos = (1280/2, 720/2)
    dx = Droite((0, 0, 0), (0, 0, 1))
    dy = Droite((0, 0, 0), (1, 0, 0))
    speed_rot = 700
    speed = 0.4
    menu = False
    while 1:
        if not menu:
            mouse.move(1280/2-mouse.position[0], 720/2-mouse.position[1])
        if keyboard.is_pressed("d"):
            world.move(Vec(-speed, 0, 0))
        if keyboard.is_pressed("q"):
            world.move(Vec(speed, 0, 0))
        if keyboard.is_pressed("z"):
            world.move(Vec(0, -speed, 0))
        if keyboard.is_pressed("s"):
            world.move(Vec(0, speed, 0))
        if keyboard.is_pressed("esc"):
            menu = not menu
        if not menu:
            d_posx = mouse_pos[0] - mouse.position[0]
            print(mouse.position)
            if d_posx > 0:
                world.rotate(d_posx/speed_rot, dx)
                print("1 rotating x", d_posx/speed_rot)
            elif d_posx < 0:
                world.rotate(d_posx/speed_rot, dx)
                print("-1 rotating x", d_posx/speed_rot)
            d_posy = mouse_pos[1] - mouse.position[1]
            if d_posy > 0:
                world.rotate(d_posy/speed_rot, dy)
                print("1 rotating y", d_posy/speed_rot)
            elif d_posy < 0:
                world.rotate(d_posy/100, dy)
                print("-1 rotating y", d_posy/speed_rot)
        """
        if keyboard.read_key() == "ctrl":
            for i in range(len(cube1)):
                cube1[i] = (cube1[i][0], cube1[i][1]-speed*sneak, cube1[i][2])
            sneak *= -1
        """
        if keyboard.is_pressed(" "):
            for x in range(-10, 0):
                world.move(Vec(0, 0, - ((-x / 5) ** 2 / 4)))
                world.draw()
            # sleep(0.06)
            for x in range(11):
                world.move(Vec(0, 0, (-x / 5) ** 2 / 4))
                world.draw()
        else:
            world.draw()
        mouse_pos = mouse.position


def random_gen(n_cubes, lens_point1):
    cubes = []
    for i in range(n_cubes):
        cubes.append(create_cube((randint(-10, 10), randint(-100, 500), randint(-10, 10)), 2))
    return World(cubes, lens_point1)


lens_point = (0, 0.001, 0)
cube0 = Cube(create_cube((0, 15, 0), 2))
cube2 = Cube(create_cube((10, 20, -6), 2))
world2 = World([cube0], lens_point)
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

# draw_point((0, 0))
# game_0(cube0)
# game_1(random_gen(10, lens_point))
# rotation_mouse(world2)
# (cube0)
# rotation_point((-8, 40, -4), 2, 2)
# rotation2(create_cube((-8, 40, -4), 2))
"""
for i in range(2 * 314):
    i = i / precision
    cube0 = rotation_cube(cube0, i, d1)
    cube_projection = project_cube(cube0, lens_point)
    draw_cube(cube_projection)
    draw_point((0, 0))
    turtle.update()
    sleep(0.01)
    turtle.clear()
"""

# print(matrix_multiplication([[1, 2], [1, 3]], [[1], [2]]))
world1 = World([cube0, cube2, Cube(create_cube((-8, 20, -2), 2)), Cube(create_cube((-2, 20, -6), 2)), Cube(create_cube((-2, 200, -6), 2)),
                Cube(create_cube((8, 250, -6), 2))], lens_point)
world2 = World([cube0], lens_point)


def rotation():
    p1 = [1, 10, 0]
    d1 = Droite(0, 0)
    d1.create_droite(cube0.center, (cube0.center[0], cube0.center[1]+1, cube0.center[2]))
    # d1.create_droite((0, 0, 0), (0, 0, 1))
    speed = 250
    for i in range(500):
        rotate_cube(cube0, math.pi/speed, d1)
        draw_cube(project_cube(cube0, lens_point))
        turtle.update()
        sleep(0.01)
        turtle.clear()

# rotation()
game_1(world1)

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
