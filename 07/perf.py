import time
import numpy as np

import multiply


def pymultiply(matrix_1: list, matrix_2: list):
    len1_y = len(matrix_1)
    len2_y = len(matrix_2)

    if len1_y == 0 or len2_y == 0:
        raise RuntimeError("Matrix should not be a empty.")

    len1_x = len(matrix_1[0])
    for i in range(len1_y):
        if not isinstance(matrix_1[0], list):
            raise RuntimeError("Non-list type found in list of lists.")

        if len1_x != len(matrix_1[i]):
            raise RuntimeError("Matrix should not be with variable row size.")

    len2_x = len(matrix_2[0])
    for i in range(len2_y):
        if not isinstance(matrix_2[0], list):
            raise RuntimeError("Non-list type found in list of lists.")

        if len2_x != len(matrix_2[i]):
            raise RuntimeError("Matrix should not be with variable row size.")

    if len1_x != len2_y:
        raise RuntimeError(
            "ERROR: matrices should look like (m, n) and (n, l)"
        )

    output = [[0 for _ in range(len2_x)] for _ in range(len1_y)]

    for i in range(len1_y):
        row = matrix_1[i]

        for j in range(len1_x):
            num2 = row[j]
            row_tmp = matrix_2[j]

            for k in range(len2_x):
                num1 = row_tmp[k]
                output[i][k] += num1 * num2
    return output


def main():
    A = np.random.rand(300, 400)
    B = np.random.rand(400, 500)
    a = A.tolist()
    b = B.tolist()

    print("==== python ====")
    start_ts = time.time()
    pymultiply(a, b)
    end_ts = time.time()
    print(
        "Time of execution of python multiply implementation is"
        f" {end_ts-start_ts} seconds"
    )

    print("==== capi ====")
    start_ts = time.time()
    multiply.multiply(a, b)
    end_ts = time.time()
    print(
        "Time of execution of capi multiply implementation is"
        f" {end_ts-start_ts} seconds"
    )

    print("==== numpy ====")
    start_ts = time.time()
    np.dot(A, B)
    end_ts = time.time()
    print(
        "Time of execution of numpy multiply implementation is"
        f" {end_ts-start_ts} seconds"
    )


if __name__ == "__main__":
    main()
