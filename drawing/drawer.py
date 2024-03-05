import pandas as pd
from PyQt5 import QtWidgets
from drawing.graph import Graph

NAME_WITHOUT_GAS = "Данные без вещества"
NAME_WITH_GAS = "Данные с веществом"
COLOR_WITHOUT_GAS = "#515151"
COLOR_WITH_GAS = "#DC7C02"

class Drawer(Graph):
    """ Класс для отрисовки графика"""

    def __init__(self,
                 layout: QtWidgets.QLayout,
                 widget: QtWidgets.QWidget) -> None:
        """ Инициализирует объекты графика.
        :param layout: слой для отрисовки графика.
        :param widget: виджет для отрисовки график."""
        super().__init__(
            # Слой для отрисовки графика
            layout=layout,
            # Виджет для отрисовки графика
            widget=widget
        )

    # НАЧАЛЬНЫЕ И КОНЕЧНЫЕ МОТОДЫ ОТРИСОВКИ
    def cleaning_and_chart_graph(self, x_label=None, y_label=None, title=None) -> None:
        """ Очистка и подпись графика.
        :param x_label: название оси x.
        :param y_label: название оси y.
        :param title: название графика."""
        # Возвращаем зум в домашнюю позицию
        self.toolbar.home()
        # Очищаем стек осей (от старых x, y lim)
        self.toolbar.update()
        # Очищаем график
        self.axis.clear()
        # Задаем название осей
        if x_label is not None:
            self.axis.set_xlabel(x_label)
        if y_label is not None:
            self.axis.set_ylabel(y_label)
        # Задаем название графика
        if title is not None:
            self.axis.set_title(title)

    def draw_graph(self, chart_caption: bool = False):
        """ Отрисовка (вызывается в конце).
        :param chart_caption: отображать label/имена графиков."""
        # Рисуем сетку
        self.axis.grid()
        # Инициирует отображение наименований графиков (label plot)
        if chart_caption:
            self.axis.legend()
        # Убеждаемся, что все помещается внутри холста
        self.figure.tight_layout()
        # Показываем новую фигуру в интерфейсе
        self.canvas.draw()

    # ШАБЛОНЫ ОТРИСОВКИ ГРАФИКОВ
    def no_data(self) -> None:
        """ Отрисовка без данных"""
        self.axis.text(0.5, 0.5, "Нет данных",
                       fontsize=14,
                       horizontalalignment='center',
                       verticalalignment='center')
        # Отрисовка, без подписи данных графиков
        self.draw_graph(chart_caption=False)

    def draw_line(self, data_x, data_y) -> None:
        """ Отрисовка линии.
        :param data_x: данные x.
        :param data_y: данные y."""
        # Очистка, подпись графика и осей (вызывается в начале)
        self.cleaning_and_chart_graph()

        # Рисуем график
        self.axis.plot(data_x, data_y)

        # Отрисовка (вызывается в конце)
        self.draw_graph()

    def draw_gas(
            self,
            without_substance: pd.DataFrame = pd.DataFrame(),
            with_substance: pd.DataFrame = pd.DataFrame()) -> None:
        """Отрисовка данных с веществом и без вещества

        Parameters
        ----------
        without_substance : pd.DataFrame
            данные без вещества
        with_substance : pd.DataFrame
            данные с веществом
        """
        # Наличие данных
        if with_substance.empty and without_substance.empty:
            return

        # Очистка, подпись графика и осей (вызывается в начале)
        self.cleaning_and_chart_graph()

        # Рисуем график
        if not without_substance.empty:
            self.axis.plot(
                without_substance['FREQUENCY'],
                without_substance['GAMMA'],
                label=NAME_WITHOUT_GAS,
                color=COLOR_WITHOUT_GAS,
                marker="x"
            )
        # Рисуем график
        if not with_substance.empty:
            self.axis.plot(
                with_substance['FREQUENCY'],
                with_substance['GAMMA'],
                label=NAME_WITH_GAS,
                color=COLOR_WITH_GAS,
                marker="x"
            )

        # Отрисовка (вызывается в конце)
        self.draw_graph()
