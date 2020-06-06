#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 2020-02-14
3 course, comp math
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from collections import Counter

ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
# ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LANGUAGE_SIZE = len(ALPHABET)


def idx_of_coincidence(msg: str):
    """

    :param msg: msg without spaces and punctuation
    :return: index of coincidence
    """
    c = Counter(list(msg))
    return sum(x * (x - 1) for x in c.values()) / (len(msg) * (len(msg) - 1))


def encrypt(plain_text: str, key: str):
    encrypted = ''
    key_text = (key * (len(plain_text)//len(key) + 1))[:len(plain_text)]

    for i in range(len(plain_text)):
        encrypted += ALPHABET[(ALPHABET.index(plain_text[i]) + ALPHABET.index(key_text[i])) % LANGUAGE_SIZE]

    return encrypted


def decrypt(ciphertext: str, key: str):
    decrypted = ''
    key_text = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]

    for i in range(len(ciphertext)):
        decrypted += ALPHABET[(LANGUAGE_SIZE + ALPHABET.index(ciphertext[i]) -
                               ALPHABET.index(key_text[i])) % LANGUAGE_SIZE]

    return decrypted


if __name__ == '__main__':
    enc_msg = "DTXSAOMP"
    print(decrypt(enc_msg, "LEMON"))
