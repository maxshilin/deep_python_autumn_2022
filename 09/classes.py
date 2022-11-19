import weakref
import cProfile
import pstats
import io
import gc
from memory_profiler import profile


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
    for element in lst:
        element.p_norm()


def cprof_process_list(obj):
    vec = [obj((1, 1, 1), (2, 2, 2)) for _ in range(100000)]
    [x.p_norm() for x in vec]
    del vec


def cprofile_func(obj):
    pr = cProfile.Profile()
    pr.enable()

    cprof_process_list(obj)

    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()

    print(s.getvalue())


@profile
def memprof_process_list():
    vec1 = [Vector((1, 1, 1), (2, 2, 2)) for _ in range(100000)]
    vec2 = [VectorSlots((1, 1, 1), (2, 2, 2)) for _ in range(100000)]
    vec3 = [VectorWeakref((1, 1, 1), (2, 2, 2)) for _ in range(100000)]

    del vec1
    del vec2
    del vec3
    gc.collect()


if __name__ == "__main__":
    gc.disable()

    cprofile_func(VectorSlots)
    cprofile_func(VectorSlots)
    cprofile_func(VectorWeakref)

    gc.collect()
    memprof_process_list()
    gc.enable()
