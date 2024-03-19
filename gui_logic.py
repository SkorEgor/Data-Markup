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
        self.selected = pd.DataFrame()

        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Обработчик переключения цветовой темы
        self.checkBox_color_theme.toggled.connect(self.update_color_theme)
        self.pushButton_reading_file_with_gas.clicked.connect(self.read_file_with_gas)
        self.pushButton_reading_file_without_gas.clicked.connect(self.read_file_without_gas)
        self.graph_1.figure.canvas.mpl_connect('button_press_event', self.on_click)
        self.pushButton_save_table_to_file.clicked.connect(self.save_to_file)

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

    def draw_gas(self, select: pd.DataFrame=pd.DataFrame()):
        self.graph_1.draw_gas(
            with_substance=self.data_with_gas,
            without_substance=self.data_without_gas,
            select=select
        )

    def on_click(self, event):
        if event.inaxes is not None:
            print(f"reset{self.toolbar_modes_active()}")
            if self.toolbar_modes_active():

                return

            x = event.xdata
            y = event.ydata
            print(f'Координаты: ({x:.2f}, {y:.2f})', (x, y))

            # Расчет допустимой области вокруг точки
            tolerance = 0.4  # Задаем допустимое отклонение для клика
            step_frq = self.data_with_gas['FREQUENCY'][1] - self.data_with_gas['FREQUENCY'][0]
            tolerance_frq = step_frq * tolerance

            # Индексы подходящие под условия по x
            indices = self.data_with_gas[
                self.data_with_gas['FREQUENCY'].between(x - tolerance_frq, x + tolerance_frq)
            ].index.tolist()

            if not indices:
                return
            center_index = indices[0]

            center_index = indices[0]
            window_width = int(self.lineEdit_window_width_2.text())
            self.selected = self.data_with_gas[center_index-window_width:center_index+window_width]
            print(self.selected)
            self.table()
            self.draw_gas(select=self.selected)

    # Заполение таблицы
    def table(self):
        # Нет точек поглощения - сброс
        if self.selected.empty:
            return

        # Задаем кол-во столбцов и строк
        self.tableWidget_frequency_absorption.setColumnCount(2)  # Столбцы
        self.tableWidget_frequency_absorption.setRowCount(len(self.selected))
        # Задаем название столбцов
        self.tableWidget_frequency_absorption.setHorizontalHeaderLabels(["Частота МГц", "Гамма"])

        # Заполняем таблицу
        index = 0
        for f, g in zip(
                self.selected["FREQUENCY"],
                self.selected["GAMMA"]
        ):
            # значения частоты и гаммы для 0 и 1 столбца
            self.tableWidget_frequency_absorption.setItem(index, 0, QTableWidgetItem(str('%.3f' % f)))
            self.tableWidget_frequency_absorption.setItem(index, 1, QTableWidgetItem(str('%.7E' % g)))
            index+=1

    def toolbar_modes_active(self):
        print(self.graph_1.toolbar.mode)
        # Проверка активации кнопок Zoom и Pan
        if self.graph_1.toolbar.mode in ('zoom rect', 'pan/zoom'):
            return True
        return False

    def save_to_file(self):
        print("save")
        if self.selected.empty:
            QMessageBox.warning(self, "Ошибка", "Выберите точки поглощения")
            return
        print("dialog")
        # Задаем название файла
        file_name = QFileDialog.getSaveFileName(
            None,
            'Сохранение',
            None,
            "Spectrometer Data(*.csv);;Text(*.txt);;All Files(*)"
        )[0]
        if not file_name:
            return

        self.selected.to_csv(file_name)
