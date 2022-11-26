import cProfile
import pstats
import classes


class ProfileDeco:
    def __init__(self, function):
        self.function = function
        self.prof_stats = None

    def __call__(self, *args, **kwargs):
        with cProfile.Profile() as prof:
            result = self.function(*args, **kwargs)

        if self.prof_stats is None:
            self.prof_stats = pstats.Stats(prof)
        else:
            self.prof_stats.add(prof)

        return result

    def print_stat(self):
        self.prof_stats.strip_dirs().sort_stats("cumulative").print_stats()

    def clear_stat(self):
        self.prof_stats = None


@ProfileDeco
def process_list(lst):
    for element in lst:
        element.p_norm()


if __name__ == "__main__":
    vec = [classes.Vector((1, 1, 1), (2, 2, 2)) for _ in range(100000)]

    for i in range(10):
        process_list(vec)

    process_list.print_stat()
