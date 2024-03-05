import pandas as pd
from PyQt5.QtWidgets import QFileDialog


def parser_line(line: str) -> tuple[float, float]:
    """ Парсит строку текст, получает частоту и гамму

    Parameters
    ----------
    line : str
        Строка текста с данными, разделенные пробелом
    Returns
    -------
    tuple[float, float]
        частота, гамма - данные из текста
    """
    # Разделяем строку по пробелу
    row = line.split()

    # Значения из столбцов
    frequency = float(row[1])
    gamma = float(row[4])

    # Возвращаем значения
    return frequency, gamma


def read_file(
        name_window: str = "Загрузка файла",
        file_path: str = None
) -> tuple[list[float], list[float]]:
    """ Читает из файла частоты и гаммы

    Parameters
    ----------
    name_window : str
        Название окна
    file_path : str
        Путь к файлу
    Returns
    -------
    tuple[list[float], list[float]]
        частоты, гаммы - данные из файла
    """
    # Получаем файл с данными
    if file_path is None:
        file_path = QFileDialog.getOpenFileName(None, name_window)[0]
    # Если файл не выбран - сброс
    if not file_path:
        return

    frequency, gamma = [], []
    with open(file_path, 'r') as file:
        # Пропуск строки с заголовками
        file.readline()
        # Чтение строк
        line = file.readline()
        while '*' not in line:
            # Парсим строку
            frequency_in_line, gamma_in_line = parser_line(line)
            # Добавляем в список
            frequency.append(frequency_in_line)
            gamma.append(gamma_in_line)
            # Переходим к следующей строке
            line = file.readline()

    return frequency, gamma


def freq_and_gamma_to_dataframe(
        frequency_data: list[float], gamma_data: list[float]
) -> pd.DataFrame:
    """ Создает DataFrame на основе данных частот и гамм

    Parameters
    ----------
    frequency_data : list[float]
        Список частот
    gamma_data : list[float]
        Список гамм
    Returns
    -------
    pd.DataFrame
        DataFrame со столбцами: 'FREQUENCY', 'GAMMA'
    """
    data = {'FREQUENCY': frequency_data, 'GAMMA': gamma_data}
    df = pd.DataFrame(data)
    return df
