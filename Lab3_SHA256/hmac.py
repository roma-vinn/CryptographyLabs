#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 14.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from Lab3_SHA256.sha256 import sha256
import hmac as standard_hmac
import hashlib


def hmac(key: bytes, message: bytes) -> bytes:
    b = 64  # block size in bytes

    key0 = key
    # if password is longer then block size
    if len(key) > b:
        key0 = sha256(key)  # len(key0) == 32

    key0 = key0.ljust(b, b'\x00')  # now len(key0) == b

    okeypad = bytes([k ^ 0x5c for k in key0])
    ikeypad = bytes([k ^ 0x36 for k in key0])

    return sha256(okeypad + sha256(ikeypad + message))


def test(key: bytes, message: bytes):
    print(f'For key: {key} and message: {message}')
    print(f'My hmac implementation:'.ljust(30, ' '), hmac(key, message).hex())
    print(f'Standard implementation:'.ljust(30, ' '),
          standard_hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest())


if __name__ == '__main__':
    test_key = b'thisiskey'
    test_message = b'thisismessage'
    test(test_key, test_message)
