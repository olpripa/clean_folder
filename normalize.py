import re
# transliterations of the Ukrainian alphabet in Latin.
# resolution 55 of the KMU

CYRILLIC_SYMBOLS = 'абвгґдеЄєжзиіЇїЙйклмнопрстуфхцчшщьЮюЯяэёъы'
TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "Ye", "ie", "zh", "z", "y", "i", "Yi", "i", "Y", "i",  "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "kh", "ts", "ch", "sh", "shch", "", "Yu", "iu", "Ya", "ia", "e", "", "", "y")


TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    if c.upper() in ('Є', 'Ї', 'Й', 'Ю', 'Я'):  # Ye-ie, Yi-i, Y-i, Yu-iu, Ya-ia
        continue
    else:
        TRANS[ord(c.upper())] = l.capitalize()

# print(TRANS)


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name