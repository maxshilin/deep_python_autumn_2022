def profile_deco():
    ...


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)

add.print_stat()  # выводится таблица с результатами профилирования
