#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 06.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from Lab4_RSA.miller_rabin import miller_rabin
from random import getrandbits, randint
import os
import sys


FIRST_PRIMES = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
    991, 997
)


def is_prime(n, k=12):
    for num in FIRST_PRIMES:
        if n % num == 0:
            return n == num
    mil_res = miller_rabin(n, k=k)
    return mil_res[0]


def random_prime(bit_size):
    x = getrandbits(bit_size-1) + (1 << (bit_size - 1))
    # if last bit == 0 -> x is even
    if x & 1 == 0:
        x += 1

    while not is_prime(x):
        x += 2
    return x


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mod_inv(a, b):
    """ return x such that (x * a) % b == 1 """
    g, x, _ = xgcd(a, b)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return x % b


def str_to_bin(string):
    bits = bin(int.from_bytes(string.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def bin_to_str(binary):
    n = int(binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode() or '\0'


if __name__ == '__main__':
    sys.stdout = open(os.path.basename(__file__)[:-3] + '_output.txt', "w")
    # some tests

    # random_prime / is prime
    rand_prime = random_prime(16)
    print(f"{rand_prime} is prime: {is_prime(rand_prime)}")

    # xgcd
    num1, num2 = randint(10, 100), randint(10, 100)
    gcd, c1, c2 = xgcd(num1, num2)
    print(f"{num1} * ({c1}) + {num2} * ({c2}) = {gcd}  |  {c1*num1 + c2*num2 == gcd}")

    # mod_inv
    num3, mod = randint(10, 100), random_prime(8)
    inv = mod_inv(num3, mod)
    print(f"({num3})^-1 mod {mod} = {inv}  |  {inv*num3 % mod == 1}")
