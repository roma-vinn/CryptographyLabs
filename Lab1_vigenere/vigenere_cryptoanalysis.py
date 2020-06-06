from Lab1_vigenere.vigenere_cipher import encrypt, decrypt, ALPHABET
from Lab1_vigenere.hist import get_frequency, prepare_text
from collections import Counter
# import pickle

UKR_IC = 0.0575
UKR_FREQ = {'а': 0.074, 'б': 0.018, 'в': 0.054, 'г': 0.016, 'ґ': 0.001, 'д': 0.036,
            'е': 0.017, 'є': 0.008, 'ж': 0.009, 'з': 0.024, 'и': 0.063, 'і': 0.059,
            'ї': 0.006, 'й': 0.009, 'к': 0.036, 'л': 0.037, 'м': 0.032, 'н': 0.067,
            'о': 0.097, 'п': 0.023, 'р': 0.049, 'с': 0.042, 'т': 0.057, 'у': 0.041,
            'ф': 0.001, 'х': 0.012, 'ц': 0.006, 'ч': 0.019, 'ш': 0.012, 'щ': 0.001,
            'ю': 0.004, 'я': 0.030, 'ь': 0.030}
# with open('/ukr_freq.pkl', 'rb') as fin:
#     UKR_FREQ = pickle.load(fin)


def get_ic(ciphertext):
    n = len(ciphertext)
    ic = 0
    for letter, count in Counter(ciphertext).items():
        ic += count * (count - 1)
    ic = ic / (n * (n - 1))
    return ic


def get_hi2(given_freq: dict, standard_freq: dict):
    hi2 = 0
    for letter in standard_freq:
        hi2 += (given_freq.get(letter, 0) - standard_freq[letter])**2 / standard_freq[letter]
    return hi2


def analyze_encrypted_text(text):
    opt, key = '', ''

    # find key length
    best_diff = 1
    best_len = 2
    for key_len in range(2, 33):
        indices = []
        for step in range(key_len):
            text_slice = text[step::key_len]
            if text_slice:
                indices.append(get_ic(text_slice))
        if 0 in indices:
            break
        cur_ic = sum(indices) / len(indices)
        cur_diff = abs(cur_ic - UKR_IC)
        if cur_diff < best_diff:
            best_diff = cur_diff
            best_len = key_len

    # find key of best length
    for letter_num in range(best_len):
        text_slice = text[letter_num::best_len]
        min_mse = float('+inf')
        best_letter = '-'
        for letter in ALPHABET:
            decrypted_slice = decrypt(text_slice, key=letter)
            cur_freq = get_frequency(Counter(decrypted_slice))
            cur_mse = get_hi2(cur_freq, UKR_FREQ)
            if cur_mse < min_mse:
                min_mse = cur_mse
                best_letter = letter
        key += best_letter

    opt = decrypt(text, key=key)
    return opt, key


if __name__ == '__main__':
    # text_file = '../voly.txt'
    # enc_text = encrypt(prepare_text(text_file), key='зима')
    enc_src = '../src/black_soviet_encrypted.txt'
    with open(enc_src, 'r') as file:
        enc_text = file.read()[:1000]
    print(analyze_encrypted_text(enc_text))
