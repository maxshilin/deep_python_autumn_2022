class CustomMeta(type):
    def __new__(
        cls, name, bases, classdict, **kwargs
    ):  # pylint: disable="unused-argument"
        classdict = {
            attr_name
            if attr_name[0:2] == "__" and attr_name[-1:-3:-1] == "__"
            else f"custom_{attr_name}": attr_value
            for attr_name, attr_value in classdict.items()
        }

        if "__setattr__" in classdict:
            old_setattr = classdict["__setattr__"]

            def _new_setattr(self, name, val):
                old_dict = dict(self.__dict__)
                old_setattr(self, name, val)

                new_attrs = {
                    key: self.__dict__[key]
                    for key in dict(self.__dict__)
                    if key not in old_dict.keys()
                }

                for new_name, new_val in new_attrs.items():
                    object.__delattr__(self, new_name)
                    object.__setattr__(self, f"custom_{new_name}", new_val)

            classdict["__setattr__"] = _new_setattr

        else:
            classdict[
                "__setattr__"
            ] = lambda self, name, val: super.__setattr__(
                self, f"custom_{name}", val
            )

        return super().__new__(cls, name, bases, classdict)
