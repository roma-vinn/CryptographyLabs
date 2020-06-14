#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 14.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""


class GF:
    # x^8 + x^4 + x^3 + x + 1
    _modulo = int('100011011', 2)

    def __init__(self, int_value):
        self._int_value = int_value

    @property
    def int_value(self):
        return self._int_value

    # addition is simple XOR
    def __add__(self, other):
        return GF(self.int_value ^ other.int_value)

    #
    def __mul__(self, other):
        res = 0
        for i in range(8):
            # check i-th bit
            if ((1 << i) & other.int_value) != 0:
                tmp = self.int_value
                for j in range(i):
                    tmp = tmp << 1  # mul by x is "<< 1"
                    if tmp >= 256:  # xor if needed
                        tmp ^= GF._modulo
                res ^= tmp
        return GF(res)

    def __pow__(self, power):
        power %= 255  # since x^-1 == x^255
        if self.int_value == 0 or self.int_value == 1 or power == 1:
            return self

        # if self.int_value == -1:
        #     if power % 2 == 0:
        #         return 1
        #     else:
        #         return -1

        if power == 0:
            return GF(1)

        val = self ** (power // 2)
        if power % 2 == 0:
            return GF(val * val)
        return GF(val * val * power)

    def str(self):
        return f'GF({self._int_value})'

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    a = GF(5)
    b = GF(17)
    print(a + b)
    pass
