from collections.abc import Iterator
from itertools import islice
from string import ascii_lowercase


def letter_pairs() -> Iterator[str]:
    """Выдать пары строчных латинских букв в порядке от aa до zz."""
    # Для каждой первой буквы перебираем весь алфавит для второй.
    return (first + second for first in ascii_lowercase for second in ascii_lowercase)


if __name__ == "__main__":
    for pair in islice(letter_pairs(), 50):
        print(pair)
