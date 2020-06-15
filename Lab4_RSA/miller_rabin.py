#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 08.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from random import randint
import os
import sys


def _pick_a(n, picked):
    a = randint(2, n-2)
    while a in picked:
        a = randint(2, n-2)
    return a


def miller_rabin(n: int, k=12):
    """
    Miller-Rabin primality test
    :param n: number to test
    :param k: number of iterations
    :return: (True, ) - "Probably Prime", (False, a) - (Composite, a)
    """
    picked_a = []

    # write n-1 = 2^s * m, with m odd.
    m = n-1
    s = 0
    while m % 2 == 0:
        s += 1
        m //= 2

    for j in range(k):
        a = _pick_a(n, picked_a)
        b = pow(a, m, n)
        if b != 1 and b != n-1:
            i = 1
            while i < s and b != n-1:
                b = pow(b, 2, n)
                if b == 1:
                    return False, a
                i += 1
            if b != n-1:
                return False, a
    return True,


def test(n):
    res = miller_rabin(n)
    if res[0] is True:
        print(f"{n} is probably prime")
    else:
        print(f'{n} is composite with witness for the compositeness = {res[1]}')


if __name__ == '__main__':
    sys.stdout = open(os.path.basename(__file__)[:-3] + '_output.txt', "w")
    # some tests
    test(10)  # composite
    test(11)  # prime
    test(4681)  # composite
    test(543496886068436072938449192257)  # prime
