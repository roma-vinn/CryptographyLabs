UKR_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

if __name__ == '__main__':
    plain_text = 'опдрснкнмярстомєйнлопнвнкнчдмннкдкщйяспдсщнвн'

    res = ''
    for i in range(len(plain_text)):
        res += UKR_ALPHABET[(UKR_ALPHABET.index(plain_text[i]) + 1) % 33]
    print(res)
