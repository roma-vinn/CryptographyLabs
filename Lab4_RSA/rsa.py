#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 06.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from Lab4_RSA.common import random_prime, mod_inv


class RSA:
    def __init__(self, p=None, q=None, e=65537, key_bit_size=1024):
        self.p = p
        self.q = q
        self.e = e

        # self.key_bit_size = key_bit_size
        if p is None:
            p = random_prime(key_bit_size)
        if q is None:
            q = random_prime(key_bit_size)
            while q == p:
                q = random_prime(key_bit_size)

        self.N = p*q  # public module
        self.phi = (p - 1)*(q - 1)  # totient of public module
        self.d = mod_inv(e, self.phi)  # secret exponent

    def encrypt(self, message: int):
        return pow(message, self.e, self.N)

    def decrypt(self, cryptotext: int):
        return pow(cryptotext, self.d, self.N)


if __name__ == '__main__':
    # test example from presentation
    rsa = RSA(p=11, q=23, e=3)
    m = 57
    c = rsa.encrypt(m)
    print(c)
    print(rsa.decrypt(c))

    # another test
    rsa = RSA()
    m = random_prime(64)
    c = rsa.encrypt(m)
    print(m == rsa.decrypt(c))
