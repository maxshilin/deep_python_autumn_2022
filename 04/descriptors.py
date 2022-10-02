class IntAverage:
    def __init__(self):
        self.protected_name = None

    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"

    def __get__(self, obj, objtype):
        data = getattr(obj, self.protected_name)
        if len(data) == 0:
            raise ZeroDivisionError
        return sum(data) / len(data)

    def __set__(self, obj, val):
        if not isinstance(val, list):
            raise ValueError
        for num in val:
            if not isinstance(num, int):
                raise ValueError
        setattr(obj, self.protected_name, val)


class String:
    def __init__(self):
        self.protected_name = None

    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self.protected_name)

    def __set__(self, obj, val):
        if not isinstance(val, str):
            raise ValueError
        setattr(obj, self.protected_name, val)


class PositiveInteger:
    def __init__(self):
        self.protected_name = None

    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self.protected_name)

    def __set__(self, obj, val):
        if not isinstance(val, int) or val <= 0:
            raise ValueError
        setattr(obj, self.protected_name, val)
