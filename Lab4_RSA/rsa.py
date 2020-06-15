#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 06.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from Lab4_RSA.common import random_prime, mod_inv, str_to_bin, bin_to_str
import os
import sys
from Lab3_SHA256.sha256 import sha256
from random import getrandbits


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


class OAEP_ERROR(Exception):
    pass


class OAEP:
    n = 1024
    k0 = 256

    @staticmethod
    def encrypt(plain_text):
        r = format(getrandbits(OAEP.k0), '0256b')
        plain_text = str_to_bin(plain_text)

        if len(plain_text) <= (OAEP.n - OAEP.k0):
            k1 = OAEP.n - OAEP.k0 - len(plain_text)
            zeros = plain_text + ('0' * k1)
        else:
            raise OAEP_ERROR()

        x = format(int(zeros, 2) ^ int(sha256(r.encode()).hex(), 16), '0768b')  # to 768 bits
        y = format(int(sha256(x.encode()).hex(), 16) ^ int(r, 2), '0256b')  # to 256 bits
        return x + y

    @staticmethod
    def decrypt(crypto_text):
        x = crypto_text[0:768]
        y = crypto_text[768:]

        r = format(int(y, 2) ^ int(sha256(x.encode()).hex(), 16), '0256b')  # to 256 bits
        res = format(int(x, 2) ^ int(sha256(r.encode()).hex(), 16), '0768b')  # to 768 bits

        return bin_to_str(res)


if __name__ == '__main__':
    sys.stdout = open(os.path.basename(__file__)[:-3] + '_output.txt', "w")

    # test example from presentation
    rsa = RSA(p=11, q=23, e=3)
    m = 57
    c = rsa.encrypt(m)
    print(f'For message: {m}')
    print(f'Crypto text: {c}')
    print(f'Decrypted text: {rsa.decrypt(c)}')

    # another test
    rsa = RSA()
    m = random_prime(64)
    print("Test if dec(enc(m)) == m for random m:", m == rsa.decrypt(rsa.encrypt(m)), '\n')

    msg = 'hello world'
    oaep = OAEP()
    oaep_ct = oaep.encrypt(msg)
    oaep_dec = oaep.decrypt(oaep_ct)
    print(f"For message: {msg}")
    print(f"Decrypted: {oaep_dec}")
