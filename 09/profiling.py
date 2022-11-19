import time
import classes


class ProfileDeco:
    def __init__(self, function):
        self.function = function
        self.counter = 0
        self.runtimes = []

    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        self.function(*args, **kwargs)
        runtime = time.perf_counter() - start
        self.counter += 1
        self.runtimes.append(runtime)

    def print_stat(self):
        cumulative = sum(self.runtimes)
        mean_time = cumulative / self.counter
        var = (
            sum(map(lambda x: (mean_time - x) ** 2, self.runtimes))
            / self.counter
        ) ** 0.5

        print(
            f"Number of calls: {self.counter}",
            f"Cumulative time: {cumulative:.4f} secs",
            f"Mean time: {mean_time:.4f} secs",
            f"Variance: {var:.4f} secs",
            sep="\n",
        )

    def clear_stat(self):
        self.counter = 0
        self.runtimes = []


@ProfileDeco
def process_list(lst):
    for element in lst:
        element.p_norm()


if __name__ == "__main__":
    vec = [classes.Vector((1, 1, 1), (2, 2, 2)) for _ in range(100000)]

    for i in range(10):
        process_list(vec)

    process_list.print_stat()
