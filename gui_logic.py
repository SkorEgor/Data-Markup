# coding: utf-8
import functools
import pandas as pd
from color_theme import ColorTheme
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
import matplotlib

from gui import Ui_Dialog
from drawing.graph import Graph
from drawing.drawer import Drawer
from tools_files.read_file import read_file, freq_and_gamma_to_dataframe

matplotlib.use('TkAgg')


# КЛАСС АЛГОРИТМА ПРИЛОЖЕНИЯ
class GuiProgram(Ui_Dialog):
    def __init__(self, dialog):
        # Создаем окно
        Ui_Dialog.__init__(self)
        dialog.setWindowFlags(  # Передаем флаги создания окна
            QtCore.Qt.WindowCloseButtonHint |  # Кнопка закрытия
            QtCore.Qt.WindowMaximizeButtonHint |  # Кнопка развернуть
            QtCore.Qt.WindowMinimizeButtonHint  # Кнопка свернуть
        )
        # Устанавливаем пользовательский интерфейс
        self.setupUi(dialog)

        # Параметры 1 графика
        self.graph_1 = Drawer(
            layout=self.layout_plot_1,
            widget=self.widget_plot_1
        )

        # Данные
        self.data_with_gas = pd.DataFrame()
        self.data_without_gas = pd.DataFrame()

        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Обработчик переключения цветовой темы
        self.checkBox_color_theme.toggled.connect(self.update_color_theme)
        self.pushButton_reading_file_with_gas.clicked.connect(self.read_file_with_gas)
        self.pushButton_reading_file_without_gas.clicked.connect(self.read_file_without_gas)

    # Смена цветового стиля интерфейса
    def update_color_theme(self, state):
        if state:
            self.widget_style_sheet.setStyleSheet(ColorTheme.dark_style_sheet)
        else:
            self.widget_style_sheet.setStyleSheet(ColorTheme.light_style_sheet)

    def read_file_with_gas(self):
        # Читаем файл
        data = read_file(
            name_window="Выбор файла с веществом",
            file_path="D:/5)Development/0_python/Workpieces/Interface_template/data_for_tests/25DMSO.csv"
        )
        print(data)
        if data is None:
            return

        # Конвертируем в DataFrame и заносим в класс
        self.data_with_gas = freq_and_gamma_to_dataframe(*data)
        print(self.data_with_gas)
        # Отображаем
        self.draw_gas()


    def read_file_without_gas(self):
        # Читаем файл
        data = read_file(
            name_window="Выбор файла без вещества",
            file_path="D:/5)Development/0_python/Workpieces/Interface_template/data_for_tests/25empty.csv"
        )
        if data is None:
            return
        self.data_without_gas = freq_and_gamma_to_dataframe(*data)
        # Отображаем
        self.draw_gas()

    def draw_gas(self):
        self.graph_1.draw_gas(
            with_substance=self.data_with_gas,
            without_substance=self.data_without_gas
        )

