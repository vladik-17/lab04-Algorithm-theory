from argparse import ArgumentParser
from collections.abc import Iterator
from decimal import Decimal
from itertools import islice
from string import ascii_lowercase


PAIR_LIMIT = 50
VALUE_LIMIT = 20
FUNCTION_STEP = Decimal("0.01")


def letter_pairs() -> Iterator[str]:
    """Выдать пары строчных латинских букв в порядке от aa до zz."""
    # Для каждой первой буквы перебираем весь алфавит для второй.
    return (first + second for first in ascii_lowercase for second in ascii_lowercase)


def function_values(a: float, b: float) -> Iterator[Decimal]:
    """Вычислить значения функции на отрезке [a, b] с шагом 0.01."""
    x = Decimal(str(a))
    end = Decimal(str(b))
    coefficient = Decimal("0.1")

    # Decimal позволяет прибавлять 0.01 без накопления ошибки округления.
    while x <= end:
        yield coefficient * x ** 2 + 5 * x - 2
        x += FUNCTION_STEP


def first_three_cities(line: str) -> Iterator[str]:
    cities = filter(lambda city: len(city) > 5, line.split())
    for _ in range(3):
        city = next(cities, None)
        # Если подходящих городов меньше трёх, выведем только найденные.
        if city is None:
            return
        yield city


def main() -> None:
    parser = ArgumentParser(description="Задания варианта 12")
    parser.add_argument("task", nargs="?", choices=("pairs", "values", "cities"), default="pairs")
    task = parser.parse_args().task

    if task == "pairs":
        for pair in islice(letter_pairs(), PAIR_LIMIT):
            print(pair)
    elif task == "values":
        for value in islice(function_values(-5, 7), VALUE_LIMIT):
            print(f"{value:.5f}")
    else:
        line = input("Введи названия городов через пробел\n")
        for city in first_three_cities(line):
            print(city)


if __name__ == "__main__":
    main()
