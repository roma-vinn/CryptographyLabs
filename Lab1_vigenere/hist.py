#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Roman Polishchenko at 2020-02-14
3 course, comp math
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from collections import Counter
import matplotlib.pyplot as plt
import pickle


text_file = '../src/marusya_churai.txt'
alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'


def get_frequency(letters: Counter):
    """
    Given Counter with letters and their occurrences calc proper frequencies
    :param letters: Counter
    :return: dict{letter: frequency}
    """
    total = sum(letters.values())
    frequency = dict().fromkeys(alphabet, 0)
    for letter, count in letters.items():
        frequency[letter] = count / total
    return frequency


def prepare_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read().lower()
    filtered_text = list(filter(lambda x: x in alphabet, text))
    return filtered_text


def count_letters(file_path):
    filtered_text = prepare_text(file_path)
    letters = Counter(filtered_text)
    frequency = get_frequency(letters)

    return filtered_text, frequency


if __name__ == '__main__':
    f_text, freq = count_letters(text_file)
    plt.hist(f_text, bins=32)
    plt.show()
    print(freq)
    with open('../../ukr_freq.pkl', 'wb') as fout:
        pickle.dump(freq, fout)
