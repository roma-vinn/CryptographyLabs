#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 14.06.2020
3rd course, computer mathematics
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from Lab2_AES128.GF import GF
from copy import deepcopy
from random import getrandbits
from Lab3_SHA256.sha256 import sha256
import os
import sys

# ======================= Helper functions ======================= #


def get_col(matrix, num):
    """
    Get column of matrix
    :param matrix: given matrix
    :param num: number of column
    :return: column
    """
    assert len(matrix[0]) >= num, 'num index is out of range'
    return [sub[num] for sub in matrix]


def set_col(matrix, index, col):
    assert index <= len(matrix[0]), 'index is bigger then row size'
    assert len(col) == len(matrix), 'matrix and col must have same size'

    for i in range(len(matrix)):
        matrix[i][index] = col[i]


def vector_mul(a, b):
    """ dot multiplication of two vectors """
    assert len(a) == len(b), 'a and b must have equal length'
    res = GF(0)

    for i in range(len(a)):
        res += GF(a[i]) * GF(b[i])

    return res.int_value


def vector_xor(a, b):
    """ XOR two vectors element-wise """
    assert len(a) == len(b), 'a and b must have equal length'

    res = deepcopy(a)
    for i in range(len(a)):
        res[i] ^= b[i]

    return res


def split_message(message: bytes):
    blocks_count = len(message) // 16
    for block_num in range(blocks_count):
        tmp = message[16*block_num:16*(block_num + 1)]
        m = bytes_to_matrix(tmp)
        yield m


def bytes_to_matrix(b):
    return [[b[4*i + j] for j in range(4)] for i in range(4)]


def matrix_to_bytes(m):
    res = b''
    for i in range(len(m)):
        for j in range(len(m[0])):
            hex_num = hex(m[i][j])[2:].rjust(2, '0')
            res += bytes.fromhex(hex_num)
    return res

# ======================= End of helper functions ======================= #


class AES128:
    # modes
    CBC = 0
    CTR = 1

    # TODO: generate by myself
    # sbox table for subBytes
    sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    ]

    # TODO: generate by myself
    # inverse sbox table for invSubBytes
    invsbox = [
        [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
        [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
        [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
        [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
        [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
        [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
        [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
        [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
        [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
        [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
        [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
        [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
        [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
        [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
        [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
        [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
    ]

    # matrix used for mixColumns in Galois field
    galois = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    # inverse matrix used for invMixColumns in Galois field
    invgalois = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]

    # RCon array used for Key Expansion
    rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb
    ]

    def __init__(self, key=None, mode=CBC):
        self._state = [[0 for _ in range(4)] for _ in range(4)]
        self._round_keys = [[0 for _ in range(44)] for _ in range(4)]
        self._mode = mode
        if key is None:
            # generate key using sha256
            self._generate_key()
        elif type(key) == bytes and len(key) == 16:
            self._key = AES128.prepare_text(deepcopy(key))
        elif type(key) == list and len(key) == 4 and len(key[0]) == 4:
            self._key = deepcopy(key)
        else:
            raise NotImplemented(f"Encryption is not working for such input: {key}")

        self.key_schedule()

    def _generate_key(self):
        from time import time
        tmp = sha256(str(time()))
        key = int(tmp[:128].hex()[2:].rjust(16, '0'), 16) ^ int(tmp[128:].hex()[2:].rjust(16, '0'), 16)
        key = bytes.fromhex(hex(key)[2:].rjust(32, '0'))
        self._key = AES128.prepare_text(key)

    def _encrypt(self, plain_text):
        """
        encrypt one block
        """
        # copying input data to the initial state
        if type(plain_text) == bytes and len(plain_text) == 16:
            self._state = AES128.prepare_text(deepcopy(plain_text))
        elif type(plain_text) == list and len(plain_text) == 4 and len(plain_text[0]) == 4:
            self._state = deepcopy(plain_text)
        else:
            raise NotImplemented(f"Encryption is not working for such input: {plain_text}")

        # initial round
        self.add_round_key(self._key)

        # 9 main rounds
        for i in range(1, 10):
            self.sub_bytes()
            self.shift_rows()
            self.mix_columns()
            self.add_round_key(self.sub_key(i))

        # final round
        self.sub_bytes()
        self.shift_rows()
        self.add_round_key(self.sub_key(10))

        return matrix_to_bytes(self._state)

    def encrypt(self, plain_text, iv=None):
        assert type(plain_text) != bytes or len(plain_text) % 16 == 0,\
            f'Incorrect plain text length (not divisible by 16): {len(plain_text)}.'
        if self._mode == AES128.CBC:
            if iv is None:
                iv = [[getrandbits(8) for _ in range(4)] for _ in range(4)]
            c = deepcopy(iv)
            res = matrix_to_bytes(deepcopy(iv))
            for block in split_message(plain_text):
                for i in range(4):
                    for j in range(4):
                        block[i][j] ^= c[i][j]
                enc = self._encrypt(block)
                c = enc
                res += enc
            return res
        elif self._mode == AES128.CTR:
            ctr = bytes.fromhex(hex(getrandbits(128))[2:].rjust(32, '0'))
            res = self._encrypt(ctr)  # add encrypted initial ctr value to the beginning of result

            for block in split_message(plain_text):
                enc_ctr = bytes_to_matrix(self._encrypt(ctr))
                for i in range(4):
                    for j in range(4):
                        block[i][j] ^= enc_ctr[i][j]
                res += matrix_to_bytes(block)
                ctr = (int(ctr.hex(), 16) + 1) % (1 << 128)  # increment ctr
                ctr = bytes.fromhex(hex(ctr)[2:].rjust(32, '0'))

            return res
        else:
            raise AssertionError(f'Incorrect mode: must be CBC or CTR, got {self._mode}.')

    def _decrypt(self, cipher_text):
        """
        decrypt one block
        """
        # copying input data to the initial state
        if type(cipher_text) == bytes and len(cipher_text) == 16:
            self._state = AES128.prepare_text(deepcopy(cipher_text))
        elif type(cipher_text) == list and len(cipher_text) == 4 and len(cipher_text[0]) == 4:
            self._state = deepcopy(cipher_text)
        else:
            raise NotImplemented(f"Encryption is not working for such input: {cipher_text}")

        # initial round
        self.add_round_key(self.sub_key(10))

        # 9 main rounds
        for i in range(9, 0, -1):
            self.shift_rows(inverse=True)
            self.sub_bytes(inverse=True)
            self.add_round_key(self.sub_key(i))
            self.mix_columns(inverse=True)

        # final round
        self.shift_rows(inverse=True)
        self.sub_bytes(inverse=True)
        self.add_round_key(self._key)

        return matrix_to_bytes(self._state)

    def decrypt(self, crypto_text: bytes):
        assert len(crypto_text) % 16 == 0,\
            f'Incorrect crypto text length (not divisible by 16): {len(crypto_text)}.'
        if self._mode == AES128.CBC:
            c = bytes_to_matrix(crypto_text[:16])
            res = b''
            for block in split_message(crypto_text[16:]):
                dec_block = bytes_to_matrix(self._decrypt(block))
                for i in range(4):
                    for j in range(4):
                        dec_block[i][j] ^= c[i][j]
                c = dec_block
                res += matrix_to_bytes(dec_block)
            return res
        elif self._mode == AES128.CTR:
            ctr = self._decrypt(crypto_text[:16])  # get initial ctr value from the beginning of the message
            res = b''
            for block in split_message(crypto_text[16:]):
                enc_ctr = bytes_to_matrix(self._encrypt(ctr))
                for i in range(4):
                    for j in range(4):
                        block[i][j] ^= enc_ctr[i][j]
                res += matrix_to_bytes(block)
                ctr = (int(ctr.hex(), 16) + 1) % (1 << 128)  # increment ctr
                ctr = bytes.fromhex(hex(ctr)[2:].rjust(32, '0'))

            return res
        else:
            raise AssertionError(f'Incorrect mode: must be CBC or CTR, got {self._mode}.')

    def add_round_key(self, key_matrix):
        """
        In the AddRoundKey step, the subKey is combined with the state.
        For each round, a chunk of the key scheduled is pulled; each subKey
        is the same size as the state. Each element in the byte matrix is XOR'd
        with each element in the chunk of the expanded key.
        """
        for i in range(4):
            for j in range(4):
                self._state[i][j] ^= key_matrix[i][j]

    def sub_bytes(self, inverse=False):
        """
        Replaces all elements in the passed array with values in sBox.
        :param inverse: if False - subBytes, else - invSubBytes
        """
        for i in range(4):
            for j in range(4):
                hex_num = self._state[i][j]
                if not inverse:
                    self._state[i][j] = self.sbox[hex_num // 16][hex_num % 16]
                else:
                    self._state[i][j] = self.invsbox[hex_num // 16][hex_num % 16]

    def shift_rows(self, inverse=False):
        """
        In the ShiftRows() transformation, the bytes in the last three rows of the State are cyclically
        shifted over different numbers of bytes (offsets): 0, 1, 2, 3. The first row is not shifted.
        :param inverse: if False - shiftRows, else - invShiftRows
        """
        shifted_state = deepcopy(self._state)

        # shift rows
        for i in range(4):
            for j in range(4):
                if not inverse:
                    shifted_state[i][j] = self._state[i][(j + i) % 4]
                else:
                    shifted_state[i][j] = self._state[i][(j - i + 4) % 4]

        # save result
        self._state = shifted_state

    def mix_columns(self, inverse=False):
        """
        The MixColumns() transformation operates on the State column-by-column,
        treating each column as a four-term polynomial.
        Each column multiplies by galois matrix AES.galois.
        The result replaces corresponding column in state.
        :param inverse: if False - mixColumns, else - invMixColumns
        """
        for i in range(4):
            # get i-th column
            col = get_col(self._state, i)

            for j in range(4):
                # get j-th row from galois matrix for mixColumns
                if not inverse:
                    row = AES128.galois[j]
                else:
                    row = AES128.invgalois[j]

                self._state[j][i] = vector_mul(col, row)

    def key_schedule(self):
        # save key to the 0-th position
        for i in range(4):
            for j in range(4):
                self._round_keys[i][j] = self._key[i][j]
        # generate 10 round keys
        for i in range(10):
            # get last column from previous key
            t = get_col(self._round_keys, 4 * i + 3)

            # rotate bytes
            t = t[1:] + [t[0]]

            # sub bytes
            t = list(map(lambda x: AES128.sbox[x // 16][x % 16], t))

            # XOR
            t[0] ^= AES128.rcon[i + 1]

            set_col(self._round_keys, 4*i + 4, vector_xor(get_col(self._round_keys, 4*i), t))
            set_col(self._round_keys, 4*i + 5, vector_xor(get_col(self._round_keys, 4*i + 1),
                                                          get_col(self._round_keys, 4*i + 4)))
            set_col(self._round_keys, 4*i + 6, vector_xor(get_col(self._round_keys, 4*i + 2),
                                                          get_col(self._round_keys, 4*i + 5)))
            set_col(self._round_keys, 4*i + 7, vector_xor(get_col(self._round_keys, 4*i + 3),
                                                          get_col(self._round_keys, 4*i + 6)))

    def sub_key(self, key_num):
        """
        Get key_num-th round key
        :param key_num: number of round key
        :return: round key as 4x4 matrix
        """
        cur_key = deepcopy(self._key)
        for i in range(4):
            for j in range(4):
                cur_key[i][j] = self._round_keys[i][4*key_num + j]
        return cur_key

    @staticmethod
    def prepare_text(text):
        arr = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                arr[i][j] = text[4*i + j]
        return arr


if __name__ == '__main__':
    sys.stdout = open(os.path.basename(__file__)[:-3] + '_output.txt', "w")
    # testing
    pt = b'\x32\x88\x31\xe0\x43\x5a\x31\x37\xf6\x30\x98\x07\xa8\x8d\xa2\x34'
    k = b'\x2b\x28\xab\x09\x7e\xae\xf7\xcf\x15\xd2\x15\x4f\x16\xa6\x88\x3c'

    aes = AES128(mode=AES128.CTR)
    ct = aes.encrypt(pt)
    dt = aes.decrypt(ct)

    print("plain text:".ljust(15, ' '), pt)
    print("crypto text:".ljust(15, ' '), ct)
    print("decoded text:".ljust(15, ' '), dt)

    print('\nHow changes crypto text if we change 1 bit in plain text?')
    # changed 1-st byte: 0x32 [100000] -> 0x33 [100001]
    pt_changed = b'\x33\x88\x31\xe0\x43\x5a\x31\x37\xf6\x30\x98\x07\xa8\x8d\xa2\x34'

    new_ct = aes.encrypt(pt_changed)
    print("old crypto text:".ljust(15, ' '), ct)
    print("new crypto text:".ljust(15, ' '), new_ct)

    msg = b'hello, the world'
    enc_msg = aes.encrypt(msg)
    print("message:".ljust(15, ' '), msg)
    print("crypto text:".ljust(15, ' '), enc_msg)
    print("decrypted:".ljust(15, ' '), aes.decrypt(enc_msg))
