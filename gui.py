import sys
from decimal import Decimal
from itertools import islice

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDoubleSpinBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from tasks import (
    FUNCTION_STEP,
    PAIR_LIMIT,
    VALUE_LIMIT,
    first_three_cities,
    function_values,
    letter_pairs,
)


class LabWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Лабораторная №4 · Вариант 12")
        self.resize(640, 460)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_pairs_tab(), "Пары букв")
        self.tabs.addTab(self.build_values_tab(), "Значения функции")
        self.tabs.addTab(self.build_cities_tab(), "Города")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

    def build_pairs_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.pairs_button = QPushButton("Показать пары")
        self.pairs_button.clicked.connect(self.show_pairs)
        self.pairs_output = QPlainTextEdit()
        self.pairs_output.setReadOnly(True)
        self.pairs_output.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        self.pairs_output.document().setDocumentMargin(12)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Первые 50 пар строчных латинских букв"))
        controls.addStretch()
        controls.addWidget(self.pairs_button)
        layout.addLayout(controls)
        layout.addWidget(self.pairs_output)
        return page

    def show_pairs(self) -> None:
        pairs = list(islice(letter_pairs(), PAIR_LIMIT))
        # По десять пар на строку, чтобы весь результат был виден сразу.
        rows = ["  ".join(pairs[index:index + 10]) for index in range(0, len(pairs), 10)]
        self.pairs_output.setPlainText("\n".join(rows))

    def build_values_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.a_input = self.make_bound_input(-5)
        self.b_input = self.make_bound_input(7)
        self.values_button = QPushButton("Рассчитать")
        self.values_button.clicked.connect(self.show_values)

        bounds = QHBoxLayout()
        bounds.addWidget(QLabel("Начало (a)"))
        bounds.addWidget(self.a_input)
        bounds.addWidget(QLabel("Конец (b)"))
        bounds.addWidget(self.b_input)
        bounds.addStretch()
        bounds.addWidget(self.values_button)

        self.values_status = QLabel()
        self.values_table = QTableWidget(0, 2)
        self.values_table.setHorizontalHeaderLabels(["x", "f(x)"])
        self.values_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.values_table.verticalHeader().hide()
        self.values_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout.addWidget(QLabel("f(x) = 0,1x² + 5x − 2. Шаг 0,01"))
        layout.addLayout(bounds)
        layout.addWidget(self.values_table)
        layout.addWidget(self.values_status)
        return page

    @staticmethod
    def make_bound_input(initial_value: float) -> QDoubleSpinBox:
        field = QDoubleSpinBox()
        field.setRange(-1_000_000, 1_000_000)
        field.setDecimals(2)
        field.setSingleStep(float(FUNCTION_STEP))
        field.setValue(initial_value)
        field.setFixedWidth(108)
        return field

    def show_values(self) -> None:
        a = self.a_input.value()
        b = self.b_input.value()
        self.values_table.setRowCount(0)

        if a > b:
            self.values_status.setText("Начало отрезка должно быть меньше или равно концу.")
            return

        x = Decimal(str(a))
        point = self.a_input.locale().decimalPoint()
        for row, value in enumerate(islice(function_values(a, b), VALUE_LIMIT)):
            self.values_table.insertRow(row)
            self.values_table.setItem(row, 0, QTableWidgetItem(f"{x:.2f}".replace(".", point)))
            self.values_table.setItem(row, 1, QTableWidgetItem(f"{value:.5f}".replace(".", point)))
            x += FUNCTION_STEP

        self.values_status.setText(f"Показано строк — {self.values_table.rowCount()}")

    def build_cities_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.cities_input = QLineEdit()
        self.cities_input.setPlaceholderText("Омск Москва Казань Воронеж Самара")
        self.cities_input.returnPressed.connect(self.show_cities)
        self.cities_button = QPushButton("Отобрать")
        self.cities_button.clicked.connect(self.show_cities)

        input_row = QHBoxLayout()
        input_row.addWidget(self.cities_input)
        input_row.addWidget(self.cities_button)

        self.cities_output = QListWidget()
        self.cities_output.setSpacing(3)
        self.cities_status = QLabel()
        layout.addWidget(QLabel("Названия городов через пробел"))
        layout.addLayout(input_row)
        layout.addWidget(QLabel("Первые три названия длиннее пяти символов"))
        layout.addWidget(self.cities_output)
        layout.addWidget(self.cities_status)
        return page

    def show_cities(self) -> None:
        self.cities_output.clear()
        for city in first_three_cities(self.cities_input.text()):
            self.cities_output.addItem(city)

        if self.cities_output.count() == 0:
            self.cities_status.setText("Подходящих городов нет.")
        else:
            self.cities_status.clear()


def main() -> int:
    app = QApplication(sys.argv)
    window = LabWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
