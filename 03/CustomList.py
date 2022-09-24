class CustomList(list):
    def __len__(self):
        return super().__len__()

    def __getitem__(self, i):
        return super().__getitem__(i)

    def __str__(self):
        return f"{sum(self)}:\t{super().__str__()}"

    @staticmethod
    def __apply_operator(left_number, right_number, operator):
        if operator == "+":
            return left_number + right_number
        if operator == "-":
            return left_number - right_number

    @staticmethod
    def __apply_operator_elementwise(left_operand, right_operand, operator):
        min_len = min(len(left_operand), len(right_operand))

        output = [
            CustomList.__apply_operator(
                left_operand[i], right_operand[i], operator
            )
            for i in range(min_len)
        ]

        if len(left_operand) > len(right_operand):
            output += [
                CustomList.__apply_operator(x, 0, operator)
                for x in left_operand[min_len:]
            ]

        if len(left_operand) < len(right_operand):
            output += [
                CustomList.__apply_operator(0, x, operator)
                for x in right_operand[min_len:]
            ]

        return CustomList(output)

    def __add__(self, other):
        return self.__apply_operator_elementwise(self, other, "+")

    def __radd__(self, other):
        return self.__apply_operator_elementwise(self, other, "+")

    def __iadd__(self, other):
        return self.__apply_operator_elementwise(self, other, "+")

    def __sub__(self, other):
        return self.__apply_operator_elementwise(self, other, "-")

    def __rsub__(self, other):
        return self.__apply_operator_elementwise(other, self, "-")

    def __isub__(self, other):
        return self.__apply_operator_elementwise(self, other, "-")

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def extend(self, __iterable):
        super().extend(__iterable)
        return self

    def insert(self, __index, __object):
        super().insert(__index, __object)
        return self

    def pop(self, __index):
        super().pop(__index)
        return self

    def remove(self, __value):
        super().remove(__value)
        return self

    def reverse(self):
        super().reverse()
        return self

    def sort(self, reverse=True | False, key=None):
        super().sort(reverse=reverse, key=key)
        return self
