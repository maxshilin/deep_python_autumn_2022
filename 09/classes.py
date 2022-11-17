import weakref


class Point:
    def __init__(self, x, y, z, Vector):
        self.x = x
        self.y = y
        self.z = z
        self.vector = Vector


class Vector:
    def __init__(self, point1, point2):
        self.point1 = Point(*point1, self)
        self.point2 = Point(*point2, self)

    def vec_coordinates(self):
        return (
            self.point2.x - self.point1.x,
            self.point2.y - self.point1.y,
            self.point2.z - self.point1.z,
        )

    def p_norm(self, p=2):
        return sum(map(lambda x: x**p, self.vec_coordinates())) ** (1 / p)


class PointSlots:
    __slots__ = ("x", "y", "z", "vector")

    def __init__(self, x, y, z, vector):
        self.x = x
        self.y = y
        self.z = z
        self.vector = vector


class VectorSlots:
    __slots__ = ("point1", "point2")

    def __init__(self, point1, point2):
        self.point1 = PointSlots(*point1, self)
        self.point2 = PointSlots(*point2, self)

    def vec_coordinates(self):
        return (
            self.point2.x - self.point1.x,
            self.point2.y - self.point1.y,
            self.point2.z - self.point1.z,
        )

    def p_norm(self, p=2):
        return sum(map(lambda x: x**p, self.vec_coordinates())) ** (1 / p)


class PointWeakref:
    def __init__(self, x, y, z, vector):
        self.x = x
        self.y = y
        self.z = z
        self.vector = weakref.ref(vector)


class VectorWeakref:
    def __init__(self, point1, point2):
        self.point1 = PointWeakref(*point1, self)
        self.point2 = PointWeakref(*point2, self)

    def vec_coordinates(self):
        return (
            self.point2.x - self.point1.x,
            self.point2.y - self.point1.y,
            self.point2.z - self.point1.z,
        )

    def p_norm(self, p=2):
        return sum(map(lambda x: x**p, self.vec_coordinates())) ** (1 / p)


def process_list(lst):
    for obj in lst:
        obj.p_norm()
