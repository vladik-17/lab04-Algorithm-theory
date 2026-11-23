import subprocess
import sys
from decimal import Decimal
from itertools import product
from pathlib import Path
from string import ascii_lowercase

import pytest

import tasks


# Путь берём у самого модуля, чтобы расположение теста не влияло на запуск.
TASKS_PATH = Path(tasks.__file__).resolve()


def run_tasks(*args: str, user_input: str | None = None) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(TASKS_PATH), *args],
        input=user_input,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return result.stdout.splitlines()


# Сверяем всю последовательность пар от aa до zz.
def test_letter_pairs_order_and_count():
    generator = tasks.letter_pairs()
    assert iter(generator) is generator

    expected = ["".join(pair) for pair in product(ascii_lowercase, repeat=2)]
    assert list(generator) == expected


# На отрезке из задания проверяем число значений и контрольные точки.
def test_function_values_on_assignment_interval():
    generator = tasks.function_values(-5, 7)
    assert iter(generator) is generator

    values = list(generator)
    assert len(values) == 1201
    assert values[0] == Decimal("-24.5")
    assert values[19] == Decimal("-23.73639")
    assert values[-1] == Decimal("37.9")


# Проверяем правую границу на шаге, между шагами и отрезок с a > b.
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (0.1, 0.12, [Decimal("-1.499"), Decimal("-1.44879"), Decimal("-1.39856")]),
        (0, 0.015, [Decimal("-2"), Decimal("-1.94999")]),
        (1, 0, []),
    ],
)
def test_function_values_on_short_intervals(a, b, expected):
    assert list(tasks.function_values(a, b)) == expected


# «Пермь» проверяет порог в пять букв, «Самара» — ограничение в три результата.
def test_first_three_cities_keep_input_order():
    line = "Омск Москва Пермь Казань Тула Воронеж Самара"
    assert list(tasks.first_three_cities(line)) == ["Москва", "Казань", "Воронеж"]


# Проверяем пустой ввод и строку, в которой подходит только один город.
@pytest.mark.parametrize(
    ("line", "expected"),
    [("  Омск   Москва  ", ["Москва"]), ("   ", [])],
)
def test_first_three_cities_with_fewer_matches(line, expected):
    assert list(tasks.first_three_cities(line)) == expected


# По умолчанию в терминал выводятся первые 50 пар.
def test_terminal_prints_first_50_pairs_by_default():
    output = run_tasks()
    assert len(output) == 50
    assert output[0] == "aa"
    assert output[-1] == "bx"


# Команда values выводит 20 чисел, по пять знаков после точки.
def test_terminal_prints_first_20_function_values():
    output = run_tasks("values")
    assert len(output) == 20
    assert output[0] == "-24.50000"
    assert output[-1] == "-23.73639"


# Передаём города через stdin и сверяем три строки после приглашения.
def test_terminal_reads_city_names():
    line = "Oslo Лондон Paris Berlin Rome Мадрид Lisbon Москва\n"
    output = run_tasks("cities", user_input=line)
    assert output[1:] == ["Лондон", "Berlin", "Мадрид"]
