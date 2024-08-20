import random


def slugify(text):
    idn = random.randint(1, 5000)
    text = text.lower()
    unsafe = [letter for letter in text if letter == " "]
    if unsafe:
        for letter in unsafe:
            text = text.replace(letter, '-')
    text = u'_'.join(text.split())
    text = f'{text}-{idn}'
    return text